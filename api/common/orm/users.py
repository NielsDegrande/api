"""ORM for users."""

from typing import TYPE_CHECKING, ClassVar

from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    feedbacks: Mapped["Feedbacks"] = relationship(
        "Feedbacks",
        back_populates="user",
    )
