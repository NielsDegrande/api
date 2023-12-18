"""Add sample tables.

Revision ID: ebfe4763622d
Revises: 5cfbdb83010d
Create Date: 2023-12-06 20:13:36.589865

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

from api.config import config
from db_migrations.utils.schemas import create_schema, drop_schema

revision: str = "ebfe4763622d"
down_revision: str | None = "5cfbdb83010d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade to newer version."""
    create_schema(config.sample.database_schema)
    op.create_table(
        "products",
        sa.Column("product_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_name", sa.String(), nullable=False),
        sa.Column("color", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("product_id"),
        schema=config.sample.database_schema,
    )


def downgrade() -> None:
    """Downgrade to previous version."""
    drop_schema(config.sample.database_schema)
