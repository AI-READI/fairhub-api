"""remove_invite_info

Revision ID: 6173282aef08
Revises: f150341d2741
Create Date: 2023-12-19 00:32:08.157538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6173282aef08'
down_revision: Union[str, None] = 'f150341d2741'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("invite", "info")
    with op.batch_alter_table("notification") as batch_op:
        batch_op.alter_column("target", nullable=True)
