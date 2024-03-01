"""User repository."""

from fastapi import HTTPException, status
from sqlalchemy import select

from api.common.dto.user import User
from api.common.orm.users import Users
from api.utils.database import AsyncSessionLocal, orm_to_pydantic


async def read_user(username: str) -> User:
    """Get a user by its name.

    :param username: Name of user to read.
    :return: Matching user.
    """
    async with AsyncSessionLocal() as session, session.begin():
        query = select(Users).where(Users.username == username)
        result = await session.execute(query)
        user = result.scalars().first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No user with '{username}' found.",
            )

        return orm_to_pydantic(user, User)
