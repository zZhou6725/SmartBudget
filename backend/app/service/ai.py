"""AI 助手 — DeepSeek API（流式 + 票据识别 + 真实财务数据）"""
import json
import httpx
from sqlalchemy import func
from app.core.config import settings
from app.database import SessionLocal
from app.models import Budget, Expense
from app.schemas.ai import AIReply, ReceiptValidateResult, QuickPrompt

SYSTEM_PROMPT = (
    "你是 FinBalance 财衡中台的 AI 财务助手，专注于企业预算管理、费用报销、财务数据分析。"
    "你的回答应该简洁、专业，用中文回复。当涉及数据计算时给出推算过程。"
    "如果用户问的问题超出财务领域，礼貌引导回财务主题。"
    "回答中涉及金额时使用「¥」符号并保留两位小数。"
    "可以使用标题、列表等格式让回答更清晰，但不要过度使用。"
)

FINANCE_CONTEXT_TEMPLATE = """

## 当前系统真实财务数据（请据此回答用户问题）
- 预算总额：¥{total_budget:,.2f}
- 已支出总额：¥{total_expense:,.2f}
- 剩余预算：¥{remaining:,.2f}
- 整体预算使用率：{usage_rate}%
- 待审批单据数：{pending_count}
- 超预算部门数：{over_budget_count}
- 部门预算执行情况：
{department_details}

请基于以上真实数据回答用户问题。若数据不足以回答，可结合你的财务知识给出合理建议。"""

RECEIPT_PROMPT = (
    "请从以下票据文本中提取关键信息，严格按 JSON 格式返回，不要输出其他内容。\n"
    'JSON 格式：{"amount": 数字, "category": "费用类型", "date": "日期YYYY-MM-DD", "vendor": "商户名称", "confidence": 0.0~1.0}\n'
    "费用类型限：travel(差旅), office(办公用品), meal(餐饮招待), transport(交通), other(其他)\n"
    "如果某项无法识别，值设为 null 或空字符串。\n\n"
    "票据内容："
)

PRESET_PROMPTS = [
    QuickPrompt(id="1", text="本月各部门预算执行情况如何？"),
    QuickPrompt(id="2", text="哪些部门存在超预算风险？"),
    QuickPrompt(id="3", text="帮我分析最近的支出趋势"),
    QuickPrompt(id="4", text="差旅费用占比过高，给出优化建议"),
    QuickPrompt(id="5", text="如何制定下季度的预算分配方案？"),
    QuickPrompt(id="6", text="对比一下各费用类型的占比"),
]


def _get_finance_context() -> str:
    """从数据库拉取当前财务摘要数据，注入 AI 上下文"""
    db = SessionLocal()
    try:
        total_budget = float(db.query(func.sum(Budget.total_amount)).scalar() or 0)
        total_expense = float(
            db.query(func.sum(Expense.amount))
            .filter(Expense.status == "approved", Expense.deleted_at.is_(None))
            .scalar() or 0
        )
        remaining = total_budget - total_expense
        usage_rate = round(total_expense / total_budget * 100, 1) if total_budget > 0 else 0

        pending_count = (
            db.query(func.count(Expense.id))
            .filter(Expense.status == "pending", Expense.deleted_at.is_(None))
            .scalar() or 0
        )

        dept_budgets = dict(
            db.query(Budget.dept_name, func.sum(Budget.total_amount)).group_by(Budget.dept_name).all()
        )
        dept_expenses = dict(
            db.query(Expense.dept_name, func.sum(Expense.amount))
            .filter(Expense.deleted_at.is_(None))
            .group_by(Expense.dept_name).all()
        )
        over_budget_count = sum(
            1 for d, b in dept_budgets.items() if float(dept_expenses.get(d, 0)) > float(b or 0)
        )

        dept_lines = []
        for dept, budget in sorted(dept_budgets.items(), key=lambda x: float(x[1] or 0), reverse=True):
            used = float(dept_expenses.get(dept, 0))
            rate = round(used / float(budget or 0) * 100, 1) if budget else 0
            flag = "⚠️ 超预算" if used > float(budget or 0) else ""
            dept_lines.append(f"  - {dept}：预算 ¥{float(budget or 0):,.2f}，已用 ¥{used:,.2f} ({rate}%) {flag}")

        return FINANCE_CONTEXT_TEMPLATE.format(
            total_budget=total_budget,
            total_expense=total_expense,
            remaining=remaining,
            usage_rate=usage_rate,
            pending_count=pending_count,
            over_budget_count=over_budget_count,
            department_details="\n".join(dept_lines) if dept_lines else "暂无部门数据",
        )
    finally:
        db.close()


def _build_messages(user_message: str) -> list[dict]:
    context = _get_finance_context()
    return [
        {"role": "system", "content": SYSTEM_PROMPT + context},
        {"role": "user", "content": user_message},
    ]


async def chat_stream(message: str):
    """AI 对话 — 返回 SSE 异步生成器"""
    if not settings.DEEPSEEK_API_KEY:
        async def no_key():
            yield f"data: {json.dumps({'content': 'AI 助手未配置 API Key，请在 .env 中设置 DEEPSEEK_API_KEY', 'done': True})}\n\n"
        return no_key()

    return await _stream_deepseek(_build_messages(message))


async def validate_receipt(content: str) -> ReceiptValidateResult:
    """票据校验（LLM 识别）"""
    if not settings.DEEPSEEK_API_KEY:
        return ReceiptValidateResult()
    prompt = RECEIPT_PROMPT + content
    reply = await _call_deepseek_sync([{"role": "user", "content": prompt}], temperature=0.1)
    try:
        raw = reply.content.strip()
        if raw.startswith("```json"):
            raw = raw[7:]
        elif raw.startswith("```"):
            raw = raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        data = json.loads(raw.strip())
        return ReceiptValidateResult(
            amount=data.get("amount"),
            category=data.get("category", ""),
            date=data.get("date", ""),
            vendor=data.get("vendor", ""),
            confidence=data.get("confidence", 0.0),
        )
    except (json.JSONDecodeError, KeyError):
        return ReceiptValidateResult()


async def get_prompts() -> list[QuickPrompt]:
    """快捷提问列表"""
    return PRESET_PROMPTS


async def _call_deepseek_sync(messages: list[dict], temperature: float = 0.7) -> AIReply:
    """非流式调用 DeepSeek"""
    url = f"{settings.DEEPSEEK_BASE_URL}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": settings.DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 2048,
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, headers=headers, json=body)
    if resp.status_code != 200:
        return AIReply(content=f"AI 服务异常（{resp.status_code}），请稍后重试")
    data = resp.json()
    choice = data.get("choices", [{}])[0]
    msg = choice.get("message", {})
    return AIReply(
        content=msg.get("content", ""),
        thinking=msg.get("reasoning_content", ""),
        sources=[],
    )


async def _stream_deepseek(messages: list[dict]):
    """流式调用 DeepSeek，yield SSE 事件"""
    url = f"{settings.DEEPSEEK_BASE_URL}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": settings.DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2048,
        "stream": True,
    }

    async def generate():
        full_content = ""
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                async with client.stream("POST", url, headers=headers, json=body) as resp:
                    if resp.status_code != 200:
                        text = await resp.aread()
                        yield f"data: {json.dumps({'content': f'AI 服务异常（{resp.status_code}）', 'done': True})}\n\n"
                        return
                    async for line in resp.aiter_lines():
                        if not line or not line.startswith("data: "):
                            continue
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            delta = chunk["choices"][0].get("delta", {})
                            token = delta.get("content", "")
                            reasoning = delta.get("reasoning_content", "")
                            if token:
                                full_content += token
                            yield f"data: {json.dumps({'content': token, 'thinking': reasoning})}\n\n"
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue
        except Exception as e:
            yield f"data: {json.dumps({'content': f'连接异常: {str(e)}', 'done': True})}\n\n"
            return
        yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"

    return generate()