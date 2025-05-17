"""ORM for products."""

from typing import ClassVar

from sqlmodel import Field

from api.common.orm.base import Base
from api.config import config


class Products(Base, table=True):
    """ORM class to represent feedback."""

    __tablename__ = "products"
    __table_args__: ClassVar = {"schema": config.sample.database_schema}

    product_id: int | None = Field(default=None, primary_key=True)
    product_name: str
    color: str
    price: float
