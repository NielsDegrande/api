"""Add a test user to the database."""

import asyncio

import bcrypt

from api.common.orm.users import Users
from api.utils.database import AsyncSessionLocal

USERNAME = "user"
PASSWORD = "password"  # noqa: S105 - Possible hardcoded password.
ROLES = "admin"


async def add_test_user() -> None:
    """Add test user to the database."""
    password_hash = bcrypt.hashpw(PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8",
    )
    test_user = Users(username=USERNAME, password_hash=password_hash, roles=ROLES)

    async with AsyncSessionLocal() as session, session.begin():
        session.add(test_user)


asyncio.run(add_test_user())
