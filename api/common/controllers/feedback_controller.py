"""Feedback API endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.common.dto.feedback import Feedback
from api.common.dto.user import User
from api.common.services import feedback_service
from api.common.services.auth_service import authenticate_user
from api.utils.constants import ApplicationTags

feedback_router = APIRouter(
    prefix="/feedback",
    tags=[ApplicationTags.COMMON],
)


@feedback_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_feedback(
    user: Annotated[User, Depends(authenticate_user)],
    feedback: Feedback,
) -> None:
    """Send feedback.

    :param user: user.
    :param request: The feedback request.
    """
    await feedback_service.create_feedback(
        user.user_id,
        feedback,
    )
