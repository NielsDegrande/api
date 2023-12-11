"""Tests for the product controller."""

from fastapi import status
from fastapi.testclient import TestClient

from api.sample.dto.product import Product


def test__product_endpoints__expect_no_error(
    test_client: TestClient,
    basic_auth_header: str,
) -> None:
    """Validate that the `product` endpoints work end-to-end.

    :param test_client: Test client for API.
    :param basic_auth_header: Authentication header.
    """
    headers = {
        "Authorization": basic_auth_header,
    }
    product_prefix = "/api/sample/product"

    # Create a product.
    product = Product(
        product_name="test",
        color="test",
        price="5",
    )
    data = product.model_dump_json()
    response = test_client.post(
        product_prefix,
        headers=headers,
        data=data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    post_product = Product(**response.json())

    # Read all products.
    response = test_client.get(
        product_prefix,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0

    # Read a single product.
    response = test_client.get(
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
    ).model_dump_json()
    response = test_client.put(
        f"{product_prefix}/{post_product.product_id}",
        headers=headers,
        data=new_data,
    )
    assert response.status_code == status.HTTP_200_OK
    assert Product(**response.json()).price == product.price + 1

    # Delete a product.
    response = test_client.delete(
        f"{product_prefix}/{post_product.product_id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK

    # Validate deletion.
    response = test_client.get(
        f"{product_prefix}/{post_product.product_id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
