"""创建部门表+用户表

Revision ID: 003
Revises: 002
Create Date: 2026-06-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "departments",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, comment="主键ID"),
        sa.Column("name", sa.String(100), nullable=False, comment="部门名称"),
        sa.Column("manager", sa.String(50), comment="负责人"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), comment="创建时间"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, comment="主键ID"),
        sa.Column("username", sa.String(50), unique=True, nullable=False, comment="用户名"),
        sa.Column("real_name", sa.String(50), comment="真实姓名"),
        sa.Column("dept_id", sa.Integer, sa.ForeignKey("departments.id"), comment="部门ID"),
        sa.Column("role", sa.String(20), default="viewer", comment="角色"),
        sa.Column("status", sa.String(10), default="active", comment="状态"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), comment="创建时间"),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("departments")