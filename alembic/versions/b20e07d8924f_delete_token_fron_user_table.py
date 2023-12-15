"""delete_token_fron_user_table

Revision ID: b20e07d8924f
Revises: f189827ee101
Create Date: 2023-12-13 13:31:38.810816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b20e07d8924f"
down_revision: Union[str, None] = "f189827ee101"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    # if inspector.has_table("user"):
    #     if 'token' in inspector.get_columns("user"):
    op.drop_column("user", "token")
    op.drop_column("user", "token_generated")


def downgrade() -> None:
    pass
