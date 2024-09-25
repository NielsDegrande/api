"""Tests for the default controller."""

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root__expect_ok(
    async_client: AsyncClient,
    auth_header: dict[str, str],
) -> None:
    """Validate that the `root` endpoint responds with status code OK.

    :param async_client: Async client for API.
    :param auth_header: Authentication header.
    """
    async with async_client as client:
        response = await client.get("", headers=auth_header)
        assert response.status_code == status.HTTP_200_OK
        response = await client.get("/", headers=auth_header)
        assert response.status_code == status.HTTP_200_OK
        response = await client.get("/index.html", headers=auth_header)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_api_root__expect_ok(
    async_client: AsyncClient,
    auth_header: dict[str, str],
) -> None:
    """Validate that the `api_root` endpoint responds with status code OK.

    :param async_client: Async client for API.
    :param auth_header: Authentication header.
    """
    async with async_client as client:
        response = await client.get("/api", headers=auth_header)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_authenticate__expect_ok(
    async_client: AsyncClient,
    auth_header: dict[str, str],
) -> None:
    """Validate that the `authenticate` endpoint responds with status code OK.

    :param async_client: Async client for API.
    :param auth_header: Authentication header.
    """
    async with async_client as client:
        response = await client.get("/api/auth", headers=auth_header)
        assert response.status_code == status.HTTP_200_OK
        response = await client.get("/api/auth")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_check_db__expect_ok(
    async_client: AsyncClient,
    auth_header: dict[str, str],
) -> None:
    """Validate that the `db` endpoint responds with status code OK.

    :param async_client: Async client for API.
    :param auth_header: Authentication header.
    """
    async with async_client as client:
        response = await client.get("/api/db", headers=auth_header)
        assert response.status_code == status.HTTP_200_OK
