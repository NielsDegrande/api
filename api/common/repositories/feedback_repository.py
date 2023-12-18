"""Repository for feedbacks."""

from api.common.dto.feedback import Feedback
from api.common.orm.feedbacks import Feedbacks
from api.utils.database import AsyncSessionLocal


async def create_feedback(
    user_id: int,
    feedback: Feedback,
) -> None:
    """Create feedback.

    :param user_id: ID of user.
    :param feedback: Feedback to be created.
    """
    new_feedback = Feedbacks(
        user_id=user_id,
        url_path=feedback.url_path,
        feedback_message=feedback.feedback_message,
    )
    async with AsyncSessionLocal() as session, session.begin():
        session.add(new_feedback)
