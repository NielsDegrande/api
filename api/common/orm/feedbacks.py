"""ORM for feedbacks."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from api.common.orm.base import Base
from api.config import config

if TYPE_CHECKING:
    from api.common.orm.users import Users


class Feedbacks(Base):
    """ORM class to represent feedback."""

    __tablename__ = "feedbacks"
    __table_args__: ClassVar = {"schema": config.common.database_schema}

    feedback_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    url_path: Mapped[str] = mapped_column(nullable=False)
    feedback_message: Mapped[str] = mapped_column(nullable=False)
    time_created = Column(
        "time_created",
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{config.common.database_schema}.users.user_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        # Put an index on columns you will filter by often.
        index=True,
    )
    user: Mapped[Users] = relationship(
        "Users",
        back_populates="feedbacks",
    )
