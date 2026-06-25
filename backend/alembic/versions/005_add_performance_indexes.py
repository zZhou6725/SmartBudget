"""添加性能索引

Revision ID: 005
Revises: 004
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # expenses 表：最常用的复合索引 (dept_name + status + deleted_at)
    op.create_index("ix_expenses_dept_status_del", "expenses", ["dept_name", "status", "deleted_at"])
    # expenses 表：日期查询索引
    op.create_index("ix_expenses_apply_date", "expenses", ["apply_date", "status", "deleted_at"])
    # expenses 表：分类查询索引
    op.create_index("ix_expenses_category", "expenses", ["category"])
    # budgets 表：部门查询索引
    op.create_index("ix_budgets_dept_name", "budgets", ["dept_name", "year"])
    # departments 表：名称查询索引
    op.create_index("ix_departments_name", "departments", ["name"])
    # notifications 表：用户+状态索引
    op.create_index("ix_notifications_user_status", "notifications", ["user_id", "status"])


def downgrade() -> None:
    op.drop_index("ix_notifications_user_status", table_name="notifications")
    op.drop_index("ix_departments_name", table_name="departments")
    op.drop_index("ix_budgets_dept_name", table_name="budgets")
    op.drop_index("ix_expenses_category", table_name="expenses")
    op.drop_index("ix_expenses_apply_date", table_name="expenses")
    op.drop_index("ix_expenses_dept_status_del", table_name="expenses")