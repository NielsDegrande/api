"""ORM for access rights."""

from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, Relationship

from api.common.orm.base import Base
from api.config import config
from api.utils.constants import AccessLevels

if TYPE_CHECKING:
    from api.common.orm.users import Users
    from api.sample.orm.products import Products


class ProductAccessRights(Base, table=True):
    """ORM class to represent product access rights."""

    __tablename__: ClassVar[str] = "access_rights"
    __table_args__: ClassVar = {"schema": config.sample.database_schema}

    access_right_id: int | None = Field(default=None, primary_key=True)
    access_level: AccessLevels

    product_id: int = Field(
        foreign_key=f"{config.sample.database_schema}.products.product_id",
        sa_column=Column(
            ForeignKey(
                f"{config.sample.database_schema}.products.product_id",
                name="fk_products_access_rights_product_id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
    )
    concept: "Products" = Relationship()

    user_id: int = Field(
        foreign_key=f"{config.common.database_schema}.users.user_id",
        sa_column=Column(
            ForeignKey(
                f"{config.common.database_schema}.users.user_id",
                name="fk_users_access_rights_user_id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
    )
    user: "Users" = Relationship()
