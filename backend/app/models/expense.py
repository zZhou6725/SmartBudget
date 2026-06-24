"""支出表 ORM 模型"""
from datetime import datetime
from sqlalchemy import String, Integer, DECIMAL, DateTime, ForeignKey, Text, Date, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Expense(Base):
    """支出表"""
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    expense_no: Mapped[str | None] = mapped_column(String(20), comment="报销单号")
    budget_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("budgets.id"), nullable=True, comment="关联预算ID")
    dept_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="部门名称")
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="支出标题")
    category: Mapped[str | None] = mapped_column(String(20), default="other", comment="报销类型")
    amount: Mapped[float] = mapped_column(DECIMAL(15, 2), nullable=False, comment="支出金额")
    status: Mapped[str] = mapped_column(String(20), default="pending", comment="状态: draft/pending/approved/rejected")
    applicant: Mapped[str | None] = mapped_column(String(50), comment="申请人")
    apply_date: Mapped[str | None] = mapped_column(String(10), comment="申请日期")
    remark: Mapped[str | None] = mapped_column(Text, comment="备注")
    attachment_url: Mapped[str | None] = mapped_column(String(500), comment="附件地址")
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, comment="软删除时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="提交时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
