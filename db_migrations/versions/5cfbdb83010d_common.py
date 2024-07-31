"""Add common tables."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

from api.config import config
from db_migrations.utils.schemas import create_schema, drop_schema

revision: str = "5cfbdb83010d"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade to newer version."""
    create_schema(config.common.database_schema)
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("roles", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("user_id"),
        schema=config.common.database_schema,
    )

    op.create_table(
        "feedbacks",
        sa.Column("feedback_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("url_path", sa.String(), nullable=False),
        sa.Column("feedback_message", sa.String(), nullable=False),
        sa.Column("time_created", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["common.users.user_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("feedback_id"),
        schema=config.common.database_schema,
    )

    op.create_index(
        op.f("ix_common_feedbacks_user_id"),
        "feedbacks",
        ["user_id"],
        unique=False,
        schema=config.common.database_schema,
    )


def downgrade() -> None:
    """Downgrade to previous version."""
    drop_schema(config.common.database_schema)
