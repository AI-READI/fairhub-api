"""contributor_name_change

Revision ID: 31703d707dfb
Revises: 0defbfc71c59
Create Date: 2024-02-20 08:25:11.511833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31703d707dfb'
down_revision: Union[str, None] = '0defbfc71c59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("dataset_contributor", "name")
    op.add_column("dataset_contributor", sa.Column("family_name", sa.String, nullable=True))
    op.add_column("dataset_contributor", sa.Column("given_name", sa.String))
    op.execute("UPDATE dataset_contributor SET given_name = 'name'")
    with op.batch_alter_table("dataset_contributor") as batch_op:
        batch_op.alter_column("given_name", nullable=False)
