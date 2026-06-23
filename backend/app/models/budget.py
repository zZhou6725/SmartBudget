"""预算表 ORM 模型"""
from datetime import datetime
from sqlalchemy import String, Integer, DECIMAL, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Budget(Base):
    """预算表"""
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    dept_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="部门名称")
    year: Mapped[int] = mapped_column(Integer, nullable=False, comment="预算年份")
    total_amount: Mapped[float] = mapped_column(DECIMAL(15, 2), default=0.00, comment="预算总额")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )