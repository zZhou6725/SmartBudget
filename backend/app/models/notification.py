"""消息通知表 ORM 模型"""
from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Notification(Base):
    """消息通知表"""
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    type: Mapped[str] = mapped_column(String(20), nullable=False, comment="类型: alert/notice/approval")
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="消息标题")
    summary: Mapped[str | None] = mapped_column(String(500), comment="内容摘要")
    content: Mapped[str | None] = mapped_column(Text, comment="完整内容")
    status: Mapped[str] = mapped_column(String(10), default="unread", comment="状态: unread/read")
    user_id: Mapped[int | None] = mapped_column(Integer, comment="接收用户ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="创建时间")
    read_at: Mapped[datetime | None] = mapped_column(DateTime, comment="阅读时间")