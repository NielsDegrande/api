"""ORM for users."""

from typing import TYPE_CHECKING, ClassVar

from sqlalchemy.orm import (
    Mapped,
    # Pyright error: "mapped_column" is unknown import symbol.
    mapped_column,  # pyright: ignore[reportAttributeAccessIssue]
    relationship,
)

from api.common.orm.base import Base
from api.config import config

if TYPE_CHECKING:
    from api.common.orm.feedbacks import Feedbacks


class Users(Base):
    """ORM class to represent a user."""

    __tablename__ = "users"
    __table_args__: ClassVar = {"schema": config.common.database_schema}

    user_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    roles: Mapped[str] = mapped_column(nullable=True)

    # Pyright error: Expression of type "relationship"
    # cannot be assigned to declared type.
    feedbacks: Mapped["Feedbacks"] = relationship(  # pyright: ignore[reportAssignmentType]
        "Feedbacks",
        back_populates="user",
    )
