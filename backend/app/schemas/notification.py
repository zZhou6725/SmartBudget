"""消息通知 Schema（与前端 types/notification.ts 对齐）"""
from pydantic import BaseModel


class NotificationResponse(BaseModel):
    """消息记录（对齐前端 NotificationItem）"""
    id: int
    type: str
    title: str
    summary: str = ""
    content: str = ""
    status: str = "unread"
    created_at: str = ""