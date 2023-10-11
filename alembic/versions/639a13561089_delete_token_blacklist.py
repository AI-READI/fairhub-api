"""delete token_blacklist

Revision ID: 639a13561089
Revises: e6cc254fc968
Create Date: 2023-10-08 23:14:48.882104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "639a13561089"
down_revision: Union[str, None] = "e6cc254fc968"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("token_blacklist", "user_id")


def downgrade() -> None:
    pass
