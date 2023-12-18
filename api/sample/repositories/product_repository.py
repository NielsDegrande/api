"""Products repository."""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.sample.dto.product import Product
from api.sample.orm.products import Products
from api.utils.database import (
    AsyncSessionLocal,
    orm_to_pydantic,
    pydantic_to_orm,
)


async def create_product(product: Product) -> Product:
    """Create product.

    :param product: Product to create.
    :return: Created product.
    """
    new_product = pydantic_to_orm(product, Products)
    async with AsyncSessionLocal() as session, session.begin():
        session.add(new_product)
        await session.commit()
        return orm_to_pydantic(new_product, Product)


async def _get_product_by_id(product_id: int, session: AsyncSession) -> Products:
    """Get product given its ID.

    :param session: Session to use to query the database.
    :param product_id: ID of the product to read.
    :return: Matching product.
    :raises: HTTPException if no product is found.
    """
    query = select(Products).where(Products.product_id == product_id)
    result = await session.execute(query)
    product = result.scalars().first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )
    return product


async def _get_products(session: AsyncSession) -> list[Products]:
    """Get all products.

    :param session: Session to use to query the database.
    :return: All products.
    """
    query = select(Products)
    result = await session.execute(query)
    return result.scalars().all()


async def read_products() -> list[Product]:
    """Read products.

    :return: All products.
    """
    async with AsyncSessionLocal() as session, session.begin():
        return [
            orm_to_pydantic(product, Product)
            for product in await _get_products(session)
        ]


async def read_product(product_id: int) -> Product:
    """Read product by ID.

    :param product_id: ID of the product to read.
    :return: Matching product.
    """
    async with AsyncSessionLocal() as session, session.begin():
        return orm_to_pydantic(await _get_product_by_id(product_id, session), Product)


async def update_product(
    product: Product,
) -> Product:
    """Update product.

    :param product: Product to update.
    :return: Updated product.
    :raises: HTTPException if no product ID is found.
    """
    if not product.product_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product ID must be specified to update a product.",
        )

    async with AsyncSessionLocal() as session, session.begin():
        existing_product = await _get_product_by_id(
            product.product_id,
            session,
        )

        # Update fields of the existing product.
        for key, value in product.__dict__.items():
            setattr(existing_product, key, value)

        session.add(existing_product)
        await session.commit()

        return orm_to_pydantic(existing_product, Product)


async def delete_product(product_id: int) -> None:
    """Delete a product.

    :param product_id: ID of the product to delete.
    """
    async with AsyncSessionLocal() as session, session.begin():
        product = await _get_product_by_id(
            product_id,
            session,
        )
        await session.delete(product)
