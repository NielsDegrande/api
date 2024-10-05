"""Product related endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.common.dto.user import User
from api.common.services.user_service import authorize_user
from api.sample.dto.product import ProductRequest, ProductResponse, ProductUpdate
from api.sample.services import product_service
from api.utils.constants import ApplicationTag

product_router = APIRouter(
    prefix="/products",
    tags=[ApplicationTag.SAMPLE],
)


@product_router.get("")
async def get_products(
    user: Annotated[User, Depends(authorize_user)],
) -> list[ProductResponse]:
    """Get all products.

    :param user: User requesting the products.
    :return: All products.
    """
    return await product_service.get_products(user_id=user.user_id)


@product_router.get("/{product_id}")
async def get_product(
    user: Annotated[User, Depends(authorize_user)],
    product_id: int,
) -> ProductResponse:
    """Get a single product.

    :param user: User requesting the product.
    :param product_id: ID of the product to retrieve.
    :return: Product matching the provided ID.
    """
    return await product_service.get_product(
        user_id=user.user_id,
        product_id=product_id,
    )


@product_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    user: Annotated[User, Depends(authorize_user)],
    product: ProductRequest,
) -> ProductResponse:
    """Create a product.

    :param user: User creating the product.
    :param product: Product to create.
    :return: Created product.
    """
    return await product_service.create_product(
        user=user,
        product=product,
    )


@product_router.put("/{product_id}")
async def update_product(
    user: Annotated[User, Depends(authorize_user)],
    product_id: int,
    product: ProductUpdate,
) -> ProductResponse:
    """Update a product.

    :param user: User updating the product.
    :param product_id: ID of the product to update.
    :param product: Product to update.
    :return: Updated product.
    """
    return await product_service.update_product(
        user_id=user.user_id,
        product_id=product_id,
        product=product,
    )


@product_router.delete("/{product_id}")
async def delete_product(
    user: Annotated[User, Depends(authorize_user)],
    product_id: int,
) -> None:
    """Delete a product.

    :param user: User deleting the product.
    :param product_id: ID of the product to delete.
    """
    await product_service.delete_product(
        user_id=user.user_id,
        product_id=product_id,
    )
