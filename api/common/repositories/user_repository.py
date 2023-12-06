"""User repository."""

from fastapi import HTTPException, status

from api.common.dto.user import User
from api.common.orm.users import Users
from api.utils.database import database_session, orm_to_pydantic


def read_user(username: str) -> User:
    """Get a user by its name.

    :param username: Name of user to read.
    :return: user.
    """
    with database_session() as session:
        user = session.query(Users).filter_by(username=username).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No user with '{username}' found.",
            )

        return orm_to_pydantic(user, User)
