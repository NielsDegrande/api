"""ORM for feedbacks using SQLModel."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, ClassVar

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, DateTime # Keep DateTime for sa_column specific type

from api.config import config

if TYPE_CHECKING:
    from api.common.orm.users import Users  # Assuming Users will be renamed to User


class Feedbacks(SQLModel, table=True):
    """SQLModel class to represent feedback."""

    __tablename__ = "feedbacks"
    __table_args__: ClassVar = {"schema": config.common.database_schema}

    feedback_id: int | None = Field(default=None, primary_key=True) # autoincrement is True by default for PKs
    url_path: str = Field(nullable=False)
    feedback_message: str = Field(nullable=False)
    # Retain explicit DateTime(timezone=True) using sa_column for precision and timezone.
    time_created: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    user_id: int = Field(
        foreign_key=f"{config.common.database_schema}.users.user_id",
        nullable=False,
        index=True,
        sa_column_kwargs={"ondelete": "CASCADE"} # Ensure ON DELETE CASCADE is set at DB level
    )
    user: "Users" = Relationship(back_populates="feedbacks")
