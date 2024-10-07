"""Products repository."""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.sample.dto.product import ProductRequest, ProductResponse, ProductUpdate
from api.sample.orm.access_rights import ProductAccessRights
from api.sample.orm.products import Products
from api.utils.constants import AccessLevels
from api.utils.database import (
    AsyncSessionLocal,
    orm_to_pydantic,
    pydantic_to_orm,
)


async def create_product(product: ProductRequest) -> ProductResponse:
    """Create product.

    :param product: Product to create.
    :return: Created product.
    """
    new_product = pydantic_to_orm(product, Products)
    async with AsyncSessionLocal() as session, session.begin():
        session.add(new_product)
        await session.commit()
        return orm_to_pydantic(new_product, ProductResponse)


async def read_products(user_id: int) -> list[ProductResponse]:
    """Read products.

    :param user_id: ID of the user requesting the products.
    :return: All products.
    """
    async with AsyncSessionLocal() as session, session.begin():
        query = (
            select(Products)
            .join(ProductAccessRights)
            .where(ProductAccessRights.user_id == user_id)
        )
        products = (await session.execute(query)).scalars().all()
        return [orm_to_pydantic(product, ProductResponse) for product in products]


async def _read_product(
    session: AsyncSession,
    user_id: int,
    product_id: int,
    access_levels: list[AccessLevels] | None = None,
    *,
    with_for_update: bool = False,
) -> Products:
    """Read product by ID.

    :param session: Session to use to query the database.
    :param user_id: ID of the user requesting the product.
    :param product_id: ID of the product to read.
    :param access_levels: Access level required.
    :param with_for_update: Lock the document for update.
    :return: Matching product.
    :raises: HTTPException if no product is found.
    """
    query = (
        select(Products)
        .join(ProductAccessRights)
        .where(ProductAccessRights.user_id == user_id)
        .where(Products.product_id == product_id)
    )
    if access_levels:
        query = query.where(ProductAccessRights.access_level.in_(access_levels))
    if with_for_update:
        query = query.with_for_update()
    result = await session.execute(query)
    product = result.scalars().first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )
    return product


async def read_product(user_id: int, product_id: int) -> ProductResponse:
    """Read product by ID.

    :param user_id: ID of the user requesting the product.
    :param product_id: ID of the product to read.
    :return: Matching product.
    """
    async with AsyncSessionLocal() as session, session.begin():
        return orm_to_pydantic(
            await _read_product(
                session=session,
                user_id=user_id,
                product_id=product_id,
            ),
            ProductResponse,
        )


async def update_product(
    user_id: int,
    product_id: int,
    product: ProductUpdate,
) -> ProductResponse:
    """Update product.

    :param user_id: ID of the user updating the product.
    :param product_id: ID of the product to update.
    :param product: Product to update.
    :return: Updated product.
    :raises: HTTPException if no product ID is found.
    """
    if not product_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product ID must be specified to update a product.",
        )

    async with AsyncSessionLocal() as session, session.begin():
        existing_product = await _read_product(
            session=session,
            user_id=user_id,
            product_id=product_id,
            access_levels=[AccessLevels.MANAGE, AccessLevels.WRITE],
            with_for_update=True,
        )

        # Update fields of the existing product.
        for key, value in product.__dict__.items():
            if value:
                setattr(existing_product, key, value)

        session.add(existing_product)
        await session.commit()

        return orm_to_pydantic(existing_product, ProductResponse)


async def delete_product(
    user_id: int,
    product_id: int,
) -> None:
    """Delete a product.

    :param user_id: ID of the user deleting the product.
    :param product_id: ID of the product to delete.
    """
    async with AsyncSessionLocal() as session, session.begin():
        product = await _read_product(
            session=session,
            user_id=user_id,
            product_id=product_id,
            access_levels=[AccessLevels.MANAGE],
        )
        await session.delete(product)
