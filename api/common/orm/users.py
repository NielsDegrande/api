"""ORM for users using SQLModel."""

from typing import TYPE_CHECKING, ClassVar, List

from sqlmodel import Field, Relationship, SQLModel

from api.config import config

if TYPE_CHECKING:
    from api.common.orm.feedbacks import Feedbacks


class Users(SQLModel, table=True):
    """SQLModel class to represent a user."""

    __tablename__ = "users"
    __table_args__: ClassVar = {"schema": config.common.database_schema}

    user_id: int | None = Field(default=None, primary_key=True, nullable=False) # autoincrement is True by default
    username: str = Field(nullable=False)
    password_hash: str = Field(nullable=False)
    roles: str | None = Field(default=None, nullable=True) # Assuming roles can be optional

    feedbacks: List["Feedbacks"] = Relationship(back_populates="user")
