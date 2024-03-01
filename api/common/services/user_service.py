"""Authentication and authorization service."""

from functools import cache
from re import fullmatch
from typing import Annotated

from bcrypt import checkpw
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from api.common.dto.user import User
from api.common.repositories import user_repository
from api.config import config

security = HTTPBasic()


@cache
def _get_authorized_paths(roles: str) -> list[dict[str, str]]:
    """Get authorized paths given roles.

    :param roles: Roles to process.
    :return: Authorized paths.
    """
    authorized_paths = []
    for role in roles.split(","):
        for right in config.authorization.roles[role]:
            authorized_paths.extend(config.authorization.rights[right])
    return authorized_paths


async def authorize_user(
    request: Request,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> User:
    """Authenticate a user.

    :param request: Request
    :param credentials: Credentials to authenticate.
    :return: Authenticated user.
    """
    user = None
    try:
        user = await user_repository.read_user(username=credentials.username)
        authorized_paths = _get_authorized_paths(user.roles)
    except KeyError:
        message = (
            f"Username {credentials.username} does not exist"
            if not user
            else (f"Role {user.roles} does not exist.")
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
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

    # Find the authorized paths that match the requested path.
    if "api" in request.url.path and not any(
        endpoint["path"]
        for endpoint in authorized_paths
        if endpoint["method"] == request.method
        and fullmatch(endpoint["path"], request.url.path)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not have the necessary rights.",
            headers={"WWW-Authenticate": "Basic"},
        ) from None

    return user
