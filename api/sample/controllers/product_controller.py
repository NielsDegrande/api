"""Product related endpoints."""

from fastapi import APIRouter, status

from api.sample.dto.product import Product
from api.sample.services import product_service
from api.utils.constants import ApplicationTags

sample_router = APIRouter(
    prefix="/product",
    tags=[ApplicationTags.SAMPLE],
)


@sample_router.get("")
async def get_products() -> list[Product]:
    """Get all products.

    :return: All products.
    """
    return await product_service.get_products()


@sample_router.get("/{product_id}")
async def get_product(product_id: int) -> Product:
    """Get a single product.

    :param product_id: ID of the product to retrieve.
    :return: Product matching the provided ID.
    """
    return await product_service.get_product(product_id=product_id)


@sample_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product: Product,
) -> Product:
    """Create a product.

    :param product: Product to create.
    :return: Newly created product.
    """
    return await product_service.create_product(product)


@sample_router.put("/{product_id}")
async def update_product(
    product: Product,
) -> Product:
    """Update a product.

    :param product: Product to update.
    :return: Updated product.
    """
    return await product_service.update_product(product)


@sample_router.delete("/{product_id}")
async def delete_product(
    product_id: int,
) -> None:
    """Delete a product.

    :param product_id: ID of the product to delete.
    """
    await product_service.delete_product(product_id)
