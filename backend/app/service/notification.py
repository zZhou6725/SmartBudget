"""消息通知 — 真实数据库查询"""
from datetime import datetime
from app.database import SessionLocal
from app.models import Notification
from app.schemas.notification import NotificationResponse


async def get_list(
    type: str | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> tuple[list[NotificationResponse], int]:
    db = SessionLocal()
    try:
        q = db.query(Notification)
        if type:
            q = q.filter(Notification.type == type)
        if status:
            q = q.filter(Notification.status == status)
        total = q.count()
        items = q.order_by(Notification.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return [_to_response(n) for n in items], total
    finally:
        db.close()


async def get_unread_count() -> int:
    db = SessionLocal()
    try:
        return db.query(Notification).filter(Notification.status == "unread").count()
    finally:
        db.close()


async def mark_as_read(notification_id: int) -> bool:
    db = SessionLocal()
    try:
        n = db.query(Notification).filter(Notification.id == notification_id).first()
        if n and n.status == "unread":
            n.status = "read"
            n.read_at = datetime.utcnow()
            db.commit()
        return True
    finally:
        db.close()


async def mark_all_as_read() -> bool:
    db = SessionLocal()
    try:
        db.query(Notification).filter(Notification.status == "unread").update(
            {"status": "read", "read_at": datetime.utcnow()}
        )
        db.commit()
        return True
    finally:
        db.close()


async def delete(notification_id: int) -> bool:
    db = SessionLocal()
    try:
        n = db.query(Notification).filter(Notification.id == notification_id).first()
        if n:
            db.delete(n)
            db.commit()
        return True
    finally:
        db.close()


def _to_response(n: Notification) -> NotificationResponse:
    return NotificationResponse(
        id=n.id,
        type=n.type,
        title=n.title,
        summary=n.summary or "",
        content=n.content or "",
        status=n.status,
        created_at=str(n.created_at)[:19] if n.created_at else "",
    )