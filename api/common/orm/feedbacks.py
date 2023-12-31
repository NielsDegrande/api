"""ORM for feedbacks."""

from datetime import datetime
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    # Pyright error: "mapped_column" is unknown import symbol.
    mapped_column,  # pyright: ignore[reportGeneralTypeIssues]
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
    user_id: Mapped[int] = mapped_column(
        ForeignKey(f"{config.common.database_schema}.users.user_id"),
        nullable=False,
    )
    url_path: Mapped[str] = mapped_column(nullable=False)
    feedback_message: Mapped[str] = mapped_column(nullable=False)
    time_created: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
    )

    # Pyright error: Expression of type "relationship"
    # cannot be assigned to declared type.
    user: Mapped["Users"] = relationship(  # pyright: ignore[reportGeneralTypeIssues]
        "Users",
        back_populates="feedbacks",
    )
