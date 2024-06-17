"""create session table

Revision ID: 9698369d7a8c
Revises: 
Create Date: 2024-06-13 09:59:17.605666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9698369d7a8c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'session',
        sa.Column('id', sa.CHAR(36), primary_key=True),
        sa.Column('user_id', sa.CHAR(36), sa.ForeignKey("user.id"), nullable=False),
        sa.Column('expires_at', sa.BigInteger, nullable=True),
    )
