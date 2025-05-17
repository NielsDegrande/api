"""ORM for feedbacks."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship

from api.common.orm.base import Base
from api.config import config

if TYPE_CHECKING:
    from api.common.orm.users import Users


class Feedbacks(Base, table=True):
    """ORM class to represent feedback."""

    __tablename__: ClassVar[str] = "feedbacks"
    __table_args__: ClassVar = {"schema": config.common.database_schema}

    feedback_id: int | None = Field(default=None, primary_key=True)
    url_path: str
    feedback_message: str
    time_created: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            "time_created",
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    user_id: int = Field(
        foreign_key=f"{config.common.database_schema}.users.user_id",
        nullable=False,
        index=True,
    )
    # Link back to the user who submitted the feedback.
    user: "Users" = Relationship(back_populates="feedbacks")
