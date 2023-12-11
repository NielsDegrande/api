"""Add a test user to the database."""

import bcrypt

from api.common.orm.users import Users
from api.utils.database import database_session

USERNAME = "user"
PASSWORD = "password"  # noqa: S105


def add_test_user() -> None:
    """Add test user to the database."""
    password_hash = bcrypt.hashpw(PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8",
    )
    test_user = Users(username=USERNAME, password_hash=password_hash)

    with database_session() as session:
        session.add(test_user)


add_test_user()
