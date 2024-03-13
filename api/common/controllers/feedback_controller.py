"""Feedback API endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.common.dto.feedback import Feedback
from api.common.dto.user import User
from api.common.services import feedback_service
from api.common.services.user_service import authorize_user
from api.utils.constants import ApplicationTag

feedback_router = APIRouter(
    prefix="/feedback",
    tags=[ApplicationTag.COMMON],
)


@feedback_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_feedback(
    user: Annotated[User, Depends(authorize_user)],
    feedback: Feedback,
) -> None:
    """Send feedback.

    :param user: user.
    :param feedback: Feedback to send.
    """
    await feedback_service.create_feedback(
        user.user_id,
        feedback,
    )
