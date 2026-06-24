"""AI 助手 API 路由（/api/v1/ai）"""
from fastapi import APIRouter

from app.core.response import ApiResponse
from app.schemas.ai import AIChatRequest, AIReply, ReceiptValidateRequest, ReceiptValidateResult, QuickPrompt
from app.service import ai as ai_service

router = APIRouter(prefix="/ai", tags=["AI助手"])


@router.post("/chat", response_model=ApiResponse[AIReply])
async def ai_chat(data: AIChatRequest):
    """AI 对话"""
    result = await ai_service.chat(data.message)
    return ApiResponse(data=result)


@router.post("/receipt-validate", response_model=ApiResponse[ReceiptValidateResult])
async def receipt_validate(data: ReceiptValidateRequest):
    """票据校验（LLM识别）"""
    result = await ai_service.validate_receipt(data.content)
    return ApiResponse(data=result)


@router.get("/prompts", response_model=ApiResponse[list[QuickPrompt]])
async def get_prompts():
    """获取快捷提问列表"""
    data = await ai_service.get_prompts()
    return ApiResponse(data=data)