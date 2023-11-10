"""delete dataset readme table

Revision ID: 72ac2b020c7c
Revises: 
Create Date: 2023-11-08 15:47:00.205940

"""
from typing import Sequence, Union

import alembic
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "72ac2b020c7c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    alembic.op.drop_table("dataset_readme")
