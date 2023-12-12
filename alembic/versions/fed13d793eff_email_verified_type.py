"""email_verified_type

Revision ID: fed13d793eff
Revises: eee9610b2cdc
Create Date: 2023-12-05 16:03:51.166254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fed13d793eff'
down_revision: Union[str, None] = 'eee9610b2cdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('user') as batch_op:
        batch_op.alter_column('email_verified', type_=sa.Boolean(), postgresql_using="email_verified::boolean",)


def downgrade() -> None:
    pass
