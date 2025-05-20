# SQLModel models inherit directly from sqlmodel.SQLModel.
# This file (previously defining SQLAlchemy's declarative_base) is no longer needed for that purpose.
# It is kept to avoid breaking imports if other parts of the application reference it,
# though such references should ideally be updated or removed.
# For new SQLModel table definitions, see files like `api/feature/models.py` (example path).
# For base model configurations (like Pydantic settings via `model_config`),
# SQLModel allows defining a base class that inherits from SQLModel and then other models inherit from that.
# If such a shared configuration is needed, this file could be a place for that base SQLModel class.
# Example:
# from sqlmodel import SQLModel as SQLModelBase
#
# class CustomBaseModel(SQLModelBase):
#     model_config = {"validate_assignment": True}
#
# Then, in your models:
# from .base import CustomBaseModel # Assuming this file is in the same directory
# class MyTable(CustomBaseModel, table=True):
#     ...
#
# For now, it remains empty with this explanatory comment.
