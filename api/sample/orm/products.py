"""ORM for products using SQLModel."""

from typing import ClassVar, List, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from api.config import config

if TYPE_CHECKING:
    from api.sample.orm.access_rights import ProductAccessRights


class Products(SQLModel, table=True):
    """SQLModel class to represent a product."""

    __tablename__ = "products"
    __table_args__: ClassVar = {"schema": config.sample.database_schema}

    product_id: int | None = Field(default=None, primary_key=True)
    product_name: str = Field(nullable=False)
    color: str = Field(nullable=False)
    price: float = Field(nullable=False)

    # Relationship to ProductAccessRights
    # One product can have multiple access right entries associated with it.
    access_rights: List["ProductAccessRights"] = Relationship(back_populates="product")
