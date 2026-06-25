"""AI 助手 API 路由（/api/v1/ai）"""
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse

from app.core.response import ApiResponse
from app.schemas.ai import AIChatRequest, AIReply, ReceiptValidateRequest, ReceiptValidateResult, QuickPrompt
from app.service import ai as ai_service

router = APIRouter(prefix="/ai", tags=["AI助手"])


@router.post("/chat/stream")
async def ai_chat_stream(data: AIChatRequest):
    """AI 对话 — SSE 流式输出"""
    return StreamingResponse(
        await ai_service.chat_stream(data.message),
        media_type="text/event-stream",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
    )


@router.post("/receipt-validate", response_model=ApiResponse[ReceiptValidateResult])
async def receipt_validate(data: ReceiptValidateRequest):
    """票据校验（LLM识别）"""
    result = await ai_service.validate_receipt(data.content)
    return ApiResponse(data=result)


@router.post("/receipt-upload", response_model=ApiResponse[ReceiptValidateResult])
async def receipt_upload(file: UploadFile = File(...)):
    """上传票据图片/文件，LLM 识别"""
    content = await file.read()
    # 尝试以文本读取（图片暂用文件名占位，后续可接 OCR/视觉模型）
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = f"[文件: {file.filename}, 大小: {len(content)} bytes]\n请描述此票据的内容以便识别。"
    result = await ai_service.validate_receipt(text)
    return ApiResponse(data=result)


@router.get("/prompts", response_model=ApiResponse[list[QuickPrompt]])
async def get_prompts():
    """获取快捷提问列表"""
    data = await ai_service.get_prompts()
    return ApiResponse(data=data)