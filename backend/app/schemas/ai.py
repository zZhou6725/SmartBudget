"""AI 助手 Schema（与前端 types/ai.ts 字段完全对齐）"""
from pydantic import BaseModel, Field


class AIChatRequest(BaseModel):
    """AI 对话请求（对齐前端 AIChatRequest）"""
    message: str = Field(..., description="用户消息")


class AIReply(BaseModel):
    """AI 回复（对齐前端 AIReply）"""
    content: str = ""           # AI 回复内容
    thinking: str = ""          # 思考过程
    sources: list[str] = []     # 引用来源


class ReceiptValidateRequest(BaseModel):
    """票据校验请求（对齐前端 ReceiptValidateRequest）"""
    content: str = Field(..., description="票据文本/图片描述")


class ReceiptValidateResult(BaseModel):
    """票据校验结果（对齐前端 ReceiptValidateResult）"""
    amount: float | None = None  # 金额
    category: str = ""           # 费用类型
    date: str = ""               # 日期
    vendor: str = ""             # 商户名称
    confidence: float = 0.0      # 识别置信度


class QuickPrompt(BaseModel):
    """快捷提问（对齐前端 QuickPrompt）"""
    id: str
    text: str