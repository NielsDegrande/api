"""Repository for common database interactions."""

from sqlalchemy.sql import text

from api.utils.database import AsyncSessionLocal


async def check_db() -> None:
    """Run a simple query against the database."""
    async with AsyncSessionLocal() as session, session.begin():
        await session.execute(text("SELECT 1"))
