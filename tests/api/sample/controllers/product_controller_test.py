"""Tests for the product controller."""

import pytest
from fastapi import status
from httpx import AsyncClient

from api.sample.dto.product import Product


@pytest.mark.asyncio()
async def test__product_endpoints__expect_no_error(
    async_client: AsyncClient,
    basic_auth_header: str,
) -> None:
    """Validate that the `product` endpoints work end-to-end.

    :param await client: Async client for API.
    :param basic_auth_header: Authentication header.
    """
    async with async_client as client:
        headers = {
            "Authorization": basic_auth_header,
        }
        product_prefix = "/api/sample/product"

        # Create a product.
        product = Product(
            product_name="test",
            color="test",
            price=5.0,
        )
        data = product.model_dump()
        response = await client.post(
            product_prefix,
            headers=headers,
            json=data,
        )
        assert response.status_code == status.HTTP_201_CREATED
        post_product = Product(**response.json())

        # Read all products.
        response = await client.get(
            product_prefix,
            headers=headers,
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) > 0

        # Read a single product.
        response = await client.get(
            f"{product_prefix}/{post_product.product_id}",
            headers=headers,
        )
        assert response.status_code == status.HTTP_200_OK
        assert Product(**response.json()).price == product.price

        # Update a product.
        new_data = Product(
            product_id=post_product.product_id,
            product_name="test",
            color="test",
            price=product.price + 1,
        ).model_dump()
        response = await client.put(
            f"{product_prefix}/{post_product.product_id}",
            headers=headers,
            json=new_data,
        )
        assert response.status_code == status.HTTP_200_OK
        assert Product(**response.json()).price == product.price + 1

        # Delete a product.
        response = await client.delete(
            f"{product_prefix}/{post_product.product_id}",
            headers=headers,
        )
        assert response.status_code == status.HTTP_200_OK

        # Validate deletion.
        response = await client.get(
            f"{product_prefix}/{post_product.product_id}",
            headers=headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
