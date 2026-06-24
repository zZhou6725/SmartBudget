"""用户表增加密码字段

Revision ID: 004
Revises: 003
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("password", sa.String(200), nullable=False, server_default="", comment="密码哈希"))
    op.add_column("users", sa.Column("email", sa.String(100), server_default="", comment="邮箱"))
    op.add_column("users", sa.Column("phone", sa.String(20), server_default="", comment="手机号"))


def downgrade() -> None:
    op.drop_column("users", "password")