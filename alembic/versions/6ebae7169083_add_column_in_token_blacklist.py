"""add column in token_blacklist

Revision ID: 6ebae7169083
Revises: 6d4271d33834
Create Date: 2023-10-09 15:48:38.553510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ebae7169083'
down_revision: Union[str, None] = '6d4271d33834'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
