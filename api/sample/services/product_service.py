"""Service that holds product related business logic."""

from api.sample.dto.product import Product
from api.sample.repositories import product_repository


async def get_products() -> list[Product]:
    """Return all products.

    :return: All products.
    """
    return await product_repository.read_products()


async def get_product(product_id: int) -> Product:
    """Return the requested product.

    :param product_id: ID of the product to get.
    :return: Matching product.
    """
    return await product_repository.read_product(product_id=product_id)


async def create_product(
    product: Product,
) -> Product:
    """Add a product.

    :param product: Product to create.
    :return: Created product.
    """
    return await product_repository.create_product(product=product)


async def update_product(
    product: Product,
) -> Product:
    """Update product.

    :param product: Product to update.
    :return: Updated product.
    """
    return await product_repository.update_product(product=product)


async def delete_product(
    product_id: int,
) -> None:
    """Delete a product.

    :param product_id: ID of the product to delete.
    """
    await product_repository.delete_product(product_id=product_id)
