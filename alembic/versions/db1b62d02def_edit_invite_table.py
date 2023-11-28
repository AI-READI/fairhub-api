"""edit invite table

Revision ID: db1b62d02def
Revises: 72ac2b020c7c
Create Date: 2023-11-28 13:56:41.821141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'db1b62d02def'
down_revision: Union[str, None] = '72ac2b020c7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('invited_study_contributor', 'invite')
    op.add_column('invite', sa.Column('info', sa.String(), nullable=True))
    op.create_unique_constraint('study_per_user', 'invite', ['study_id', 'email_address'])
