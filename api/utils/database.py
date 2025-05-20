"""Database utilities."""

import sys

from box import Box
from sqlalchemy.pool import NullPool, QueuePool # SQLModel uses standard QueuePool
# SQLModel import removed as it's not directly used after removing TypeVars
from sqlmodel.ext.asyncio.session import AsyncSession, create_async_engine # Updated imports
from sqlalchemy.orm import sessionmaker # For creating AsyncSessionLocal
# TypeVar import removed as it's no longer used

from api.config import config


def create_connection_string(db_config: Box = config.database) -> str:
    """Create the environment specific connection string.

    :param db_config: Database configuration.
    :return: String representation of the connection string.
    """
    # Non-empty environment indicates we run on a hosted environment.
    if config.environment:
        return (
            f"{db_config.dialect}://"
            f"{db_config.username}:{db_config.password}@/"
            f"{db_config.db_name}"
            f"?unix_sock={db_config.unix_socket_path}"
        )
    # Else, return the local database connection string.
    return (
        f"{db_config.dialect}://"
        f"{db_config.username}:{db_config.password}@"
        f"{db_config.host}:{db_config.port}/"
        f"{db_config.db_name}"
    )


engine = create_async_engine(
    create_connection_string(),
    future=True,
    # AsyncIO pytest works with NullPool.
    # SQLModel's create_async_engine handles async adaptation, so use QueuePool directly.
    poolclass=NullPool if "pytest" in sys.modules else QueuePool,
)

# Create an async session maker using SQLModel's AsyncSession
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# SQLModel models are Pydantic models. These helper functions are no longer needed.
# TypeVarBaseModel and TypeVarORMModel are also removed as they were only used by these functions.
