"""Repository for feedbacks, using SQLModel."""

from pydantic import BaseModel

from api.common.orm.feedbacks import Feedbacks # SQLModel ORM class
# Assuming Feedback DTO can be used as a Pydantic schema for creation
from api.common.dto.feedback import Feedback as FeedbackCreateSchema 
from api.common.repositories.default_repository import DefaultRepository


# Define a Pydantic model for updating feedbacks.
# Only fields that can be updated should be included.
# All fields should be optional.
class FeedbackUpdateSchema(BaseModel):
    url_path: str | None = None
    feedback_message: str | None = None
    # user_id is typically not updatable for an existing feedback record.
    # time_created is also not typically updatable.


class FeedbackRepository(DefaultRepository[Feedbacks, FeedbackUpdateSchema]):
    """
    Repository for managing feedback records.
    It uses Feedbacks as the ORM model and FeedbackUpdateSchema for update operations.
    For creation, the service layer will typically convert a FeedbackCreateSchema (or DTO)
    into a Feedbacks model instance before calling the create method.
    """

    def __init__(self) -> None:
        """Initialize the feedback repository."""
        super().__init__(Feedbacks)

    # The create, get_by_id, get_all, update, delete methods are inherited from DefaultRepository.
    # DefaultRepository.create expects a 'Feedbacks' model instance.
    # DefaultRepository.update expects a 'FeedbackUpdateSchema' instance.

    # If we need a method that specifically takes the FeedbackCreateSchema (like the old create_feedback function)
    # and handles the ORM object creation, it can be added here.
    async def create_feedback_from_schema(
        self, user_id: int, feedback_data: FeedbackCreateSchema
    ) -> Feedbacks:
        """
        Create a new feedback record from schema data.

        :param user_id: ID of the user submitting the feedback.
        :param feedback_data: The feedback data from the DTO/schema.
        :return: The created Feedbacks ORM instance.
        """
        feedback_orm = Feedbacks(
            user_id=user_id,
            url_path=feedback_data.url_path,
            feedback_message=feedback_data.feedback_message,
            # time_created will be handled by default_factory in Feedbacks model
        )
        # Use the inherited create method
        return await self.create(feedback_orm)

# Example of how it might be used (e.g., in a service layer):
# feedback_repo = FeedbackRepository()
# new_feedback_dto = FeedbackCreateSchema(url_path="/home", feedback_message="Great!")
# created_feedback_orm = await feedback_repo.create_feedback_from_schema(user_id=1, feedback_data=new_feedback_dto)
#
# existing_feedback_to_update = await feedback_repo.get_by_id(some_id)
# if existing_feedback_to_update:
#     update_dto = FeedbackUpdateSchema(feedback_message="Actually, it was awesome!")
#     updated_feedback = await feedback_repo.update(entity_id=some_id, data_update=update_dto)

# The original create_feedback function is now effectively replaced by
# instantiating FeedbackRepository and calling its create_feedback_from_schema method (or create method directly).
