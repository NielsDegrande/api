"""ORM for access rights."""

from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    # Pyright error: "mapped_column" is unknown import symbol.
    mapped_column,  # pyright: ignore[reportAttributeAccessIssue]
    relationship,
)

from api.common.orm.base import Base
from api.config import config
from api.utils.constants import AccessLevels

if TYPE_CHECKING:
    from api.common.orm.users import Users
    from api.sample.orm.products import Products


class ProductAccessRights(Base):
    """ORM class to represent product access rights."""

    __tablename__ = "access_rights"
    __table_args__: ClassVar = {"schema": config.sample.database_schema}

    access_right_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    access_level: Mapped[AccessLevels] = mapped_column(nullable=False)

    product_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{config.sample.database_schema}.products.product_id",
            name="fk_products_access_rights_product_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    # Pyright error: Expression of type "relationship"
    # cannot be assigned to declared type.
    concept: Mapped["Products"] = relationship(  # pyright: ignore[reportAssignmentType]
        "Products",
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{config.common.database_schema}.users.user_id",
            name="fk_users_access_rights_user_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    # Pyright error: Expression of type "relationship"
    # cannot be assigned to declared type.
    user: Mapped["Users"] = relationship(  # pyright: ignore[reportAssignmentType]
        "Users",
    )
