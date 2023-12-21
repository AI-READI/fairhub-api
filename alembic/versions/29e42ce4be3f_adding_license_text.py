"""adding license text

Revision ID: 29e42ce4be3f
Revises: 72ac2b020c7c
Create Date: 2023-12-21 13:34:26.478808

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29e42ce4be3f'
down_revision: Union[str, None] = '72ac2b020c7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("dataset_rights", sa.Column("license_text", sa.String, nullable=True))
    op.execute(
        "UPDATE dataset_rights SET license_text = ''"
    )
    with op.batch_alter_table("dataset_rights") as batch_op:
        batch_op.alter_column("license_text", nullable=False)
