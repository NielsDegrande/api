"""Add access control."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

from api.config import config

revision: str = "7c3b60d312ff"
down_revision: str | None = "ebfe4763622d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade to newer version."""
    op.create_table(
        "access_rights",
        sa.Column("access_right_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "access_level",
            sa.Enum("MANAGE", "READ", "WRITE", name="accesslevels"),
            nullable=False,
        ),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["sample.products.product_id"],
            name="fk_products_access_rights_product_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["common.users.user_id"],
            name="fk_users_access_rights_user_id",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("access_right_id"),
        schema=config.sample.database_schema,
    )


def downgrade() -> None:
    """Downgrade to previous version."""
    op.execute("DROP TYPE IF EXISTS accesslevels CASCADE")
    op.drop_table("access_rights", schema=config.sample.database_schema)
