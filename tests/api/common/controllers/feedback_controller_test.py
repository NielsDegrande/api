"""Tests for the feedback controller."""

from fastapi import status
from fastapi.testclient import TestClient

from api.common.dto.feedback import Feedback


def test_create_feedback__expect_created(
    test_client: TestClient,
    basic_auth_header: str,
) -> None:
    """Validate that the `feedback` endpoint responds with status code CREATED.

    :param test_client: Test client for API.
    :param basic_auth_header: Authentication header.
    """
    headers = {
        "Authorization": basic_auth_header,
    }
    data = Feedback(
        feedback_message="test",
        url_path="test",
    ).model_dump_json()
    response = test_client.post(
        "/api/feedback",
        headers=headers,
        data=data,
    )
    assert response.status_code == status.HTTP_201_CREATED
