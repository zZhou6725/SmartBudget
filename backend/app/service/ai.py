"""AI 助手 业务逻辑层（当前返回空占位数据，后续对接 LLM）"""
from app.schemas.ai import AIReply, ReceiptValidateResult, QuickPrompt


async def chat(message: str) -> AIReply:
    """AI 对话 — 后续对接 LLM API"""
    return AIReply()


async def validate_receipt(content: str) -> ReceiptValidateResult:
    """票据校验 — 后续对接 LLM 识别引擎"""
    return ReceiptValidateResult()


async def get_prompts() -> list[QuickPrompt]:
    """快捷提问列表"""
    return []