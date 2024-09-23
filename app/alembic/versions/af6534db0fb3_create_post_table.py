"""create_post_table

Revision ID: af6534db0fb3
Revises: 
Create Date: 2024-09-23 11:53:25.398910

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af6534db0fb3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('published', sa.Boolean, server_default='TRUE'),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('posts')
    
