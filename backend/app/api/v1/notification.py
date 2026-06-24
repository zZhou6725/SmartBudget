"""消息通知 API 路由（/api/v1/notifications）"""
from fastapi import APIRouter, Query

from app.core.response import ApiResponse, PageResult
from app.schemas.notification import NotificationResponse
from app.service import notification as notification_service

router = APIRouter(prefix="/notifications", tags=["消息通知"])


@router.get("", response_model=ApiResponse[PageResult[NotificationResponse]])
async def list_notifications(
    type: str | None = Query(None, description="类型筛选"),
    status: str | None = Query(None, description="状态筛选"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    """分页查询消息列表"""
    items, total = await notification_service.get_list(type, status, page, page_size)
    return ApiResponse(data=PageResult(items=items, total=total, page=page, page_size=page_size))


@router.get("/unread-count", response_model=ApiResponse[int])
async def unread_count():
    """未读消息数量"""
    count = await notification_service.get_unread_count()
    return ApiResponse(data=count)


@router.put("/{notification_id}/read", response_model=ApiResponse)
async def mark_as_read(notification_id: int):
    """标记已读"""
    await notification_service.mark_as_read(notification_id)
    return ApiResponse(msg="已标记")


@router.put("/read-all", response_model=ApiResponse)
async def mark_all_as_read():
    """全部已读"""
    await notification_service.mark_all_as_read()
    return ApiResponse(msg="全部已读")


@router.delete("/{notification_id}", response_model=ApiResponse)
async def delete_notification(notification_id: int):
    """删除消息"""
    await notification_service.delete(notification_id)
    return ApiResponse(msg="删除成功")