"""edit invite table PK

Revision ID: 95d6e53e2578
Revises: db1b62d02def
Create Date: 2023-11-28 14:58:43.869472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "95d6e53e2578"
down_revision: Union[str, None] = "db1b62d02def"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    connection = op.get_bind()
    inspector = sa.inspect(connection)

    # Check if the table exists before dropping it
    if inspector.has_table("invite"):
        op.add_column("invite", sa.Column("id", sa.CHAR(36), nullable=True))
        op.execute(
            "UPDATE invite SET id = uuid_in(overlay(overlay(md5(random()::text || ':' "
            "|| random()::text) placing '4' from 13) placing to_hex(floor(random()*(11-8+1) + 8)::int)"
            "::text from 17)::cstring);"
        )
        op.execute("ALTER TABLE invite DROP CONSTRAINT invited_study_contributor_pkey")

        op.create_primary_key("id", "invite", ["id"])
        with op.batch_alter_table("invite") as batch_op:
            batch_op.alter_column("study_id", nullable=True)
