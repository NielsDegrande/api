"""ORM for products."""

from typing import ClassVar

from sqlalchemy.orm import Mapped, mapped_column

from api.common.orm.base import Base
from api.config import config


class Products(Base):
    """ORM class to represent feedback."""

    __tablename__ = "products"
    __table_args__: ClassVar = {"schema": config.sample.database_schema}

    product_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    product_name: Mapped[str] = mapped_column(nullable=False)
    color: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
