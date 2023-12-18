"""Tests for the feedback controller."""

import pytest
from fastapi import status
from httpx import AsyncClient

from api.common.dto.feedback import Feedback


@pytest.mark.asyncio()
async def test_create_feedback__expect_created(
    async_client: AsyncClient,
    basic_auth_header: str,
) -> None:
    """Validate that the `feedback` endpoint responds with status code CREATED.

    :param async_client: Async client for API.
    :param basic_auth_header: Authentication header.
    """
    headers = {
        "Authorization": basic_auth_header,
    }
    data = Feedback(
        feedback_message="test",
        url_path="test",
    ).model_dump()

    async with async_client as client:
        response = await client.post(
            "/api/feedback",
            headers=headers,
            json=data,
        )
    assert response.status_code == status.HTTP_201_CREATED
