"""消息通知 业务逻辑层（当前返回空占位数据）"""
from app.schemas.notification import NotificationResponse


async def get_list(
    type: str | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> tuple[list[NotificationResponse], int]:
    return [], 0


async def get_unread_count() -> int:
    return 0


async def mark_as_read(notification_id: int) -> bool:
    return True


async def mark_all_as_read() -> bool:
    return True


async def delete(notification_id: int) -> bool:
    return True