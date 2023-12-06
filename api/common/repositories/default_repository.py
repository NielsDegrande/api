"""Repository for common database interactions."""

from sqlalchemy.sql import text

from api.utils.database import database_session


async def check_db() -> None:
    """Run a simple query against the database."""
    with database_session() as session:
        session.execute(text("SELECT 1"))
