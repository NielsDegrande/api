"""Feedback service."""
from api.common.dto.feedback import Feedback
from api.common.repositories import feedback_repository


async def create_feedback(
    user_id: int,
    request: Feedback,
) -> None:
    """Create feedback.

    :param user_id: ID of user.
    :param request: The feedback request.
    """
    await feedback_repository.create_feedback(user_id, request)
