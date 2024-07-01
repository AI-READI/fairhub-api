"""email verified type

Revision ID: 3ffefbd9c03b
Revises: 9698369d7a8c
Create Date: 2024-07-01 12:28:02.596192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ffefbd9c03b'
down_revision: Union[str, None] = '9698369d7a8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("user") as batch_op:
        batch_op.alter_column(
            "email_verified",
            type_=sa.Boolean(),
            postgresql_using="email_verified::boolean",
        )






