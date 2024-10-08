"""Data transfer objects for product."""

from pydantic import BaseModel, Field


class ProductRequest(BaseModel):
    """Request to create a product."""

    product_name: str
    color: str
    price: float = Field(ge=0.0)


class ProductUpdate(BaseModel):
    """Request to update a product."""

    product_name: str | None = None
    color: str | None = None
    price: float | None = Field(default=None, ge=0.0)


class ProductResponse(ProductRequest):
    """Response holding a product."""

    product_id: int
