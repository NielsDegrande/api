"""Products repository."""

from fastapi import HTTPException, status

from api.sample.dto.product import Product
from api.sample.orm.products import Products
from api.utils.database import (
    Session,
    database_session,
    orm_to_pydantic,
    pydantic_to_orm,
)


def create_product(product: Product) -> Product:
    """Create product.

    :param product: Product to create.
    :return: Created product.
    """
    new_product = pydantic_to_orm(product, Products)
    with database_session() as session:
        session.add(new_product)
        session.commit()
        return orm_to_pydantic(new_product, Product)


def _get_product_by_id(product_id: int, session: Session) -> Products:
    """Get product given its ID.

    :param session: Session to use to query the database.
    :param product_id: ID of the product to read.
    :return: Matching product.
    :raises: HTTPException if no product is found.
    """
    product = session.query(Products).filter(Products.product_id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )
    return product


def _get_products(session: Session) -> list[Products]:
    """Get all products.

    :param session: Session to use to query the database.
    :return: All products.
    """
    return session.query(Products).all()


def read_products() -> list[Product]:
    """Read products.

    :return: All products.
    """
    with database_session() as session:
        return [orm_to_pydantic(product, Product) for product in _get_products(session)]


def read_product(product_id: int) -> Product:
    """Read product by ID.

    :param product_id: ID of the product to read.
    :return: Matching product.
    """
    with database_session() as session:
        return orm_to_pydantic(_get_product_by_id(product_id, session), Product)


def update_product(
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

    with database_session() as session:
        existing_product = _get_product_by_id(
            product.product_id,
            session,
        )

        # Update fields of the existing product.
        for key, value in product.__dict__.items():
            setattr(existing_product, key, value)

        session.add(existing_product)
        session.commit()

        return orm_to_pydantic(existing_product, Product)


def delete_product(product_id: int) -> None:
    """Delete a product.

    :param product_id: ID of the product to delete.
    """
    with database_session() as session:
        product = _get_product_by_id(
            product_id,
            session,
        )
        session.delete(product)
