"""ORM for access rights using SQLModel."""

from typing import TYPE_CHECKING, ClassVar
# Assuming AccessLevels is a Python Enum, we need sqlalchemy.Enum for persistence
from sqlalchemy import Column, Enum 
from sqlmodel import Field, Relationship, SQLModel

from api.config import config
from api.utils.constants import AccessLevels # This needs to be a Python Enum

if TYPE_CHECKING:
    from api.common.orm.users import Users
    from api.sample.orm.products import Products # Ensure this will be SQLModel version


class ProductAccessRights(SQLModel, table=True):
    """SQLModel class to represent product access rights."""

    __tablename__ = "access_rights"
    __table_args__: ClassVar = {"schema": config.sample.database_schema}

    access_right_id: int | None = Field(default=None, primary_key=True)
    # Assuming AccessLevels is a Python Enum and needs to be stored as such.
    # If AccessLevels is just a string type alias, remove sa_column and use `access_level: str`.
    access_level: AccessLevels = Field(
        sa_column=Column(Enum(AccessLevels)), nullable=False
    )

    # Assuming product_id in Products table is int. This will be confirmed when products.py is updated.
    product_id: int = Field(
        foreign_key=f"{config.sample.database_schema}.products.product_id",
        # name="fk_products_access_rights_product_id" is not directly settable in Field, 
        # but the FK constraint will be named by the DB or SQLAlchemy based on convention.
        sa_column_kwargs={"ondelete": "CASCADE"},
        nullable=False,
    )
    # Renaming 'concept' to 'product' for clarity, assuming it links to a Product.
    product: "Products" = Relationship() # No back_populates defined in original

    user_id: int = Field(
        foreign_key=f"{config.common.database_schema}.users.user_id",
        # name="fk_users_access_rights_user_id" - similar to above, name handled by convention.
        sa_column_kwargs={"ondelete": "CASCADE"},
        nullable=False,
    )
    user: "Users" = Relationship() # No back_populates defined in original
