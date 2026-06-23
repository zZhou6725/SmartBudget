"""初始迁移：创建预算表 + 支出表

Revision ID: 001
Revises: None
Create Date: 2026-06-23
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """创建 budgets 预算表"""
    op.create_table(
        "budgets",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, comment="主键ID"),
        sa.Column("dept_name", sa.String(100), nullable=False, comment="部门名称"),
        sa.Column("year", sa.Integer, nullable=False, comment="预算年份"),
        sa.Column(
            "total_amount",
            sa.DECIMAL(15, 2),
            default=0.00,
            comment="预算总额",
        ),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), comment="创建时间"),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), comment="更新时间"),
    )

    """创建 expenses 支出表"""
    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, comment="主键ID"),
        sa.Column(
            "budget_id",
            sa.Integer,
            sa.ForeignKey("budgets.id"),
            nullable=True,
            comment="关联预算ID",
        ),
        sa.Column("dept_name", sa.String(100), nullable=False, comment="部门名称"),
        sa.Column("title", sa.String(200), nullable=False, comment="支出标题"),
        sa.Column("amount", sa.DECIMAL(15, 2), nullable=False, comment="支出金额"),
        sa.Column(
            "status",
            sa.String(20),
            default="pending",
            comment="状态: pending/approved/rejected",
        ),
        sa.Column("applicant", sa.String(50), comment="申请人"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), comment="提交时间"),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), comment="更新时间"),
    )


def downgrade() -> None:
    op.drop_table("expenses")
    op.drop_table("budgets")