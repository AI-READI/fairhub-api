"""add token to user

Revision ID: df71df391cdb
Revises: 3ffefbd9c03b
Create Date: 2024-07-03 10:15:49.657807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df71df391cdb'
down_revision: Union[str, None] = '3ffefbd9c03b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
