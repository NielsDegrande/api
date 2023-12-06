"""Authentication service."""

from typing import Annotated

from bcrypt import checkpw
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from api.common.dto.user import User
from api.common.repositories import user_repository as users_repository

security = HTTPBasic()


async def authenticate_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> User:
    """Authenticate a user.

    :param credentials: Credentials to authenticate.
    :return: Authenticated user.
    """
    try:
        user = users_repository.read_user(username=credentials.username)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username does not exist.",
            headers={"WWW-Authenticate": "Basic"},
        ) from None

    if not checkpw(
        credentials.password.encode("utf-8"),
        user.password_hash.encode("utf-8"),
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password.",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user
