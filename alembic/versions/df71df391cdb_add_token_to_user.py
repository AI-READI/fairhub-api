"""add token to user

Revision ID: df71df391cdb
Revises: 3ffefbd9c03b
Create Date: 2024-07-03 10:15:49.657807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = 'df71df391cdb'
down_revision: Union[str, None] = '0ff53a655198'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

password_reset_token = str(uuid.uuid4())

def upgrade() -> None:
    op.add_column(
        "user", sa.Column("password_reset_token", sa.String, nullable=True)
    )
