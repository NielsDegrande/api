"""Tests for the default controller."""

from fastapi import status
from fastapi.testclient import TestClient


def test_root__expect_ok(
    test_client: TestClient,
    basic_auth_header: str,
) -> None:
    """Validate that the `root` endpoint responds with status code OK.

    :param test_client: Test client for API.
    :param basic_auth_header: Authentication header.
    """
    headers = {
        "Authorization": basic_auth_header,
    }

    response = test_client.get("", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = test_client.get("/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = test_client.get("/index.html", headers=headers)
    assert response.status_code == status.HTTP_200_OK


def test_api_root__expect_ok(
    test_client: TestClient,
    basic_auth_header: str,
) -> None:
    """Validate that the `api_root` endpoint responds with status code OK.

    :param test_client: Test client for API.
    :param basic_auth_header: Authentication header.
    """
    headers = {
        "Authorization": basic_auth_header,
    }

    response = test_client.get("/api", headers=headers)
    assert response.status_code == status.HTTP_200_OK


def test_authenticate__expect_ok(
    test_client: TestClient,
    basic_auth_header: str,
) -> None:
    """Validate that the `authenticate` endpoint responds with status code OK.

    :param test_client: Test client for API.
    :param basic_auth_header: Authentication header.
    """
    headers = {
        "Authorization": basic_auth_header,
    }

    response = test_client.get("/auth", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = test_client.get("/auth")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_check_db__expect_ok(
    test_client: TestClient,
    basic_auth_header: str,
) -> None:
    """Validate that the `db` endpoint responds with status code OK.

    :param test_client: Test client for API.
    :param basic_auth_header: Authentication header.
    """
    headers = {
        "Authorization": basic_auth_header,
    }

    response = test_client.get("/api/db", headers=headers)
    assert response.status_code == status.HTTP_200_OK
