"""user_table_email_verfication

Revision ID: f189827ee101
Revises: fed13d793eff
Create Date: 2023-12-11 14:54:31.303523

"""
from typing import Sequence, Union
import sqlalchemy as sa
import datetime
import random
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f189827ee101"
down_revision: Union[str, None] = "fed13d793eff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
token_generated = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
token = random.randint(10 ** (7 - 1), (10**7) - 1)


def upgrade():
    op.add_column("user", sa.Column("token_generated", sa.BIGINT, nullable=True))
    op.add_column("user", sa.Column("token", sa.String, nullable=True))
    op.execute(f"UPDATE \"user\" SET token_generated ='{token_generated}'")
    op.execute(f"UPDATE \"user\" SET token ='{token}'")
    op.execute("UPDATE invite SET info ='info'")
    op.execute(f'UPDATE "user" SET email_verified = FALSE')

    with op.batch_alter_table("user") as batch_op:
        batch_op.alter_column("token", nullable=False)
        batch_op.alter_column("token_generated", nullable=False)
        batch_op.alter_column("email_verified", nullable=False)
    with op.batch_alter_table("invite") as batch_op:
        batch_op.alter_column("info", nullable=False)
