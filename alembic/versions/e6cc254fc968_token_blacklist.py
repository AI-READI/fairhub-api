"""token_blacklist

Revision ID: e6cc254fc968
Revises: 3e48c46694c8
Create Date: 2023-10-06 19:40:38.517323

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e6cc254fc968"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("token_blacklist", sa.Column("user_id", sa.String, nullable=True))


def downgrade() -> None:
    pass
