"""Data transfer objects representing product access rights."""

from pydantic import BaseModel

from api.utils.constants import AccessLevels


class ProductAccessRightRequest(BaseModel):
    """Request to create an access right."""

    product_id: int
    access_level: AccessLevels


class ProductAccessRightResponse(ProductAccessRightRequest):
    """Response holding an access right."""

    access_right_id: int
    user_id: int
    username: str
