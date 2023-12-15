"""role_nullable_and_fk_user_id

Revision ID: eee9610b2cdc
Revises: 95d6e53e2578
Create Date: 2023-12-01 00:09:44.745776

"""
from typing import Sequence, Union

import sqlalchemy as sa
import datetime
import uuid
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "eee9610b2cdc"
down_revision: Union[str, None] = "95d6e53e2578"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

created_at = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

id = str(uuid.uuid4())
hashed = str(uuid.uuid4())


def upgrade() -> None:
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    if inspector.has_table("invite"):
        op.add_column("invite", sa.Column("user_id", sa.CHAR(36)))
        op.execute(
            f'INSERT INTO "user" ("id", "email_address", "username", "hash", "created_at", "email_verified") VALUES '
            f"('{id}', 'eee9610b2cdc@fairhub.io', 'eee9610b2cdc', '{hashed}', '{created_at}', 0)"
        )

        user_obj = f"SELECT * FROM user WHERE id = '{id}'"
        if len(user_obj) < 1:
            return "error", 403
        op.execute(f"UPDATE invite SET user_id ='{id}'")

        with op.batch_alter_table("invite") as batch_op:
            batch_op.alter_column("permission", nullable=True)
            batch_op.alter_column("user_id", nullable=False)
        op.create_foreign_key(
            "fk_user_id",
            "invite",
            "user",
            ["user_id"],
            ["id"],
        )

        with op.batch_alter_table("notification") as batch_op:
            batch_op.alter_column("title", nullable=False)
            batch_op.alter_column("message", nullable=False)
            batch_op.alter_column("type", nullable=False)
            batch_op.alter_column("target", nullable=False)
            batch_op.alter_column("read", nullable=False)
