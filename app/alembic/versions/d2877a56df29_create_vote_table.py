"""create_vote_table

Revision ID: d2877a56df29
Revises: 5d6bedd5d56c
Create Date: 2024-09-25 10:16:20.338764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2877a56df29'
down_revision: Union[str, None] = '5d6bedd5d56c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "votes",
        sa.Column("post_id", sa.Integer, nullable=False),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("post_id", "user_id")
    )

def downgrade() -> None:
    op.drop_table("votes")
