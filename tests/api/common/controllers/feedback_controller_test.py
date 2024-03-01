"""Tests for the feedback controller."""

import pytest
from fastapi import status
from httpx import AsyncClient

from api.common.dto.feedback import Feedback


@pytest.mark.asyncio()
async def test_create_feedback__expect_created(
    async_client: AsyncClient,
    auth_header: dict[str, str],
) -> None:
    """Validate that the `feedback` endpoint responds with status code CREATED.

    :param async_client: Async client for API.
    :param auth_header: Authentication header.
    """
    data = Feedback(
        feedback_message="test",
        url_path="test",
    ).model_dump()

    async with async_client as client:
        response = await client.post(
            "/api/feedback",
            headers=auth_header,
            json=data,
        )
    assert response.status_code == status.HTTP_201_CREATED
