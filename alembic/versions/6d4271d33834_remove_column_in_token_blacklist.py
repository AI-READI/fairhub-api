"""remove column in token_blacklist

Revision ID: 6d4271d33834
Revises: 32e5ff331a78
Create Date: 2023-10-09 11:11:58.478289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6d4271d33834"
down_revision: Union[str, None] = "32e5ff331a78"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("token_blacklist", "user_id")


def downgrade() -> None:
    pass
