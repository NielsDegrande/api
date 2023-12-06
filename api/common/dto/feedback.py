"""Data transfer objects for the feedback endpoints."""

from pydantic import BaseModel


class Feedback(BaseModel):
    """DTO to represent a feedback.

    :param feedback_message: Feedback message.
    :param url_path: Path to the page on which the feedback was submitted.
    """

    feedback_message: str
    url_path: str
