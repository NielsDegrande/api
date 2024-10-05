"""Service that holds product related business logic."""

from api.common.dto.user import User
from api.sample.dto.product import ProductRequest, ProductResponse, ProductUpdate
from api.sample.repositories import access_right_repository, product_repository
from api.utils.constants import AccessLevels


async def get_products(user_id: int) -> list[ProductResponse]:
    """Get all products.

    :param user_id: ID of the user requesting the products.
    :return: All products.
    """
    return await product_repository.read_products(user_id=user_id)


async def get_product(user_id: int, product_id: int) -> ProductResponse:
    """Get the requested product.

    :param user_id: ID of the user requesting the product.
    :param product_id: ID of the product to get.
    :return: Matching product.
    """
    return await product_repository.read_product(
        user_id=user_id,
        product_id=product_id,
    )


async def create_product(
    user: User,
    product: ProductRequest,
) -> ProductResponse:
    """Create a product.

    :param user: User creating the product.
    :param product: Product to create.
    :return: Created product.
    """
    product = await product_repository.create_product(
        product=product,
    )
    await access_right_repository.create_access_right(
        product_id=product.product_id,
        user=user,
        access_level=AccessLevels.MANAGE,
    )
    return product


async def update_product(
    user_id: int,
    product_id: int,
    product: ProductUpdate,
) -> ProductResponse:
    """Update a product.

    :param user_id: ID of the user updating the product.
    :param product_id: ID of the product to update.
    :param product: Product to update.
    :return: Updated product.
    """
    return await product_repository.update_product(
        user_id=user_id,
        product_id=product_id,
        product=product,
    )


async def delete_product(
    user_id: int,
    product_id: int,
) -> None:
    """Delete a product.

    :param user_id: ID of the user updating the product.
    :param product_id: ID of the product to delete.
    """
    await product_repository.delete_product(
        user_id=user_id,
        product_id=product_id,
    )
