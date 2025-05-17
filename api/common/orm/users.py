"""ORM for users."""

from typing import TYPE_CHECKING, ClassVar

from sqlmodel import Field, Relationship

from api.common.orm.base import Base
from api.config import config

if TYPE_CHECKING:
    from api.common.orm.feedbacks import Feedbacks


class Users(Base, table=True):
    """ORM class to represent a user."""

    __tablename__ = "users"
    __table_args__: ClassVar = {"schema": config.common.database_schema}

    user_id: int | None = Field(default=None, primary_key=True)
    username: str
    password_hash: str
    roles: str | None = None

    # Relationship to feedback entries for this user.
    feedbacks: list["Feedbacks"] = Relationship(back_populates="user")
