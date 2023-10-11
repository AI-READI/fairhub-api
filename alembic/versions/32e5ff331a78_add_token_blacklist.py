"""add token_blacklist

Revision ID: 32e5ff331a78
Revises: 639a13561089
Create Date: 2023-10-09 11:10:06.568148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "32e5ff331a78"
down_revision: Union[str, None] = "639a13561089"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("token_blacklist", sa.Column("user_id", sa.String, nullable=True))


def downgrade() -> None:
    pass
