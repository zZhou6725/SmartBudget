"""用户表 ORM"""
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="用户名")
    real_name: Mapped[str | None] = mapped_column(String(50), comment="真实姓名")
    dept_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("departments.id"), comment="部门ID")
    role: Mapped[str] = mapped_column(String(20), default="viewer", comment="角色")
    password: Mapped[str] = mapped_column(String(200), nullable=False, comment="密码哈希")
    email: Mapped[str | None] = mapped_column(String(100), default="", comment="邮箱")
    phone: Mapped[str | None] = mapped_column(String(20), default="", comment="手机号")
    status: Mapped[str] = mapped_column(String(10), default="active", comment="状态: active/disabled")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="创建时间")