"""add_posts_users_relation

Revision ID: 5d6bedd5d56c
Revises: e61c8ff0133d
Create Date: 2024-09-24 15:59:09.261549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d6bedd5d56c'
down_revision: Union[str, None] = 'e61c8ff0133d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add owner_id column to posts table
    # Add relation between posts and users
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    
    op.create_foreign_key(
        "fk_posts_users",
        "posts",
        "users",
        ["owner_id"],
        ["id"]
    )


def downgrade() -> None:
    op.drop_constraint("fk_posts_users", "posts", type_="foreignkey")
    op.drop_column("posts", "owner_id")
