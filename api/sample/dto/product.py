"""Data transfer objects for product."""

from pydantic import BaseModel, Field


class Product(BaseModel):
    """DTO to represent a product.

    :param product_id: Product ID.
    :param product_name: Name of the product.
    :param color: Product color.
    :param price: Product price.
    """

    product_id: int | None
    product_name: str
    color: str
    price: int = Field(ge=0)
