"""modify_email_verification

Revision ID: f150341d2741
Revises: b20e07d8924f
Create Date: 2023-12-13 20:43:24.637259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f150341d2741'
down_revision: Union[str, None] = 'b20e07d8924f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('email_verification', 'token', type_=sa.String)
    op.alter_column('email_verification', 'user_id', type_=sa.CHAR(36))
    op.alter_column('email_verification', 'created_at', type_=sa.BIGINT)
