"""Service that holds product related business logic."""

from api.sample.dto.product import Product
from api.sample.repositories import product_repository


async def get_product(product_id: int | None) -> list[Product]:
    """Return the requested product or all if None is specified.

    :param product_id: ID of the product to get.
    :return: Matching products.
    """
    return product_repository.read_product(product_id=product_id)


async def create_product(
    product: Product,
) -> Product:
    """Add a product.

    :param product: Product to create.
    :return: Created product.
    """
    return product_repository.create_product(product=product)


async def update_product(
    product: Product,
) -> Product:
    """Update product.

    :param product: Product to update.
    :return: Updated product.
    """
    return product_repository.update_product(product=product)


async def delete_product(
    product_id: int,
) -> None:
    """Delete a product.

    :param product_id: ID of the product to delete.
    """
    product_repository.delete_product(product_id=product_id)
