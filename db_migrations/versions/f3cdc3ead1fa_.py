"""Add roles column to users table.

Revision ID: f3cdc3ead1fa
Revises: ebfe4763622d
Create Date: 2023-12-18 16:14:27.654913

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

from api.config import config

revision: str = "f3cdc3ead1fa"
down_revision: str | None = "ebfe4763622d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade to newer version."""
    op.add_column(
        "users",
        sa.Column("roles", sa.String(), nullable=True),
        schema=config.common.database_schema,
    )


def downgrade() -> None:
    """Downgrade to previous version."""
    op.drop_column(
        "users",
        "roles",
        schema=config.common.database_schema,
    )
