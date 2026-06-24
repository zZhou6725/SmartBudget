"""创建消息通知表

Revision ID: 002
Revises: 001
Create Date: 2026-06-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, comment="主键ID"),
        sa.Column("type", sa.String(20), nullable=False, comment="类型: alert/notice/approval"),
        sa.Column("title", sa.String(200), nullable=False, comment="消息标题"),
        sa.Column("summary", sa.String(500), comment="内容摘要"),
        sa.Column("content", sa.Text, comment="完整内容"),
        sa.Column("status", sa.String(10), default="unread", comment="状态: unread/read"),
        sa.Column("user_id", sa.Integer, comment="接收用户ID"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), comment="创建时间"),
        sa.Column("read_at", sa.DateTime, comment="阅读时间"),
    )


def downgrade() -> None:
    op.drop_table("notifications")