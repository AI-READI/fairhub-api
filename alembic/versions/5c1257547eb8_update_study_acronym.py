"""update_study_acronym

Revision ID: 5c1257547eb8
Revises: 3ffefbd9c03b
Create Date: 2025-02-19 16:25:24.597207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c1257547eb8'
down_revision: Union[str, None] = '3ffefbd9c03b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("study") as batch_op:
        batch_op.alter_column(
            "acronym",
            new_column_name="short_description",
            type_=sa.String(300),
            nullable=False
        )
