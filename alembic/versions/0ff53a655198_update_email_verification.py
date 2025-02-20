"""update_email_verification

Revision ID: 0ff53a655198
Revises: 3ffefbd9c03b
Create Date: 2025-02-18 13:50:48.808176

"""
from typing import Sequence, Union
import sqlalchemy as sa
import datetime
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '0ff53a655198'
down_revision: Union[str, None] = '5c1257547eb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


created_at = int(datetime.datetime.now(datetime.timezone.utc).timestamp())


def upgrade() -> None:
    op.alter_column("email_verification", "token", type_=sa.String)
    op.alter_column("email_verification", "user_id", type_=sa.CHAR(36))

    op.drop_column("email_verification", "created_at")

    op.add_column(
        "email_verification", sa.Column("created_at", sa.BIGINT(), nullable=True)
    )

    op.execute(f"UPDATE \"email_verification\" SET created_at ='{created_at}'")

    op.alter_column("email_verification", "created_at", nullable=False)
