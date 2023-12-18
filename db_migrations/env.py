"""Alembic environment specification."""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import AsyncConnection

from api.common.orm.base import Base
from api.utils.database import create_connection_string, engine

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here
# for 'autogenerate' support.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we do not even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = create_connection_string()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Required as we are using a non-default schema.
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def _run_sync_migration(connection: AsyncConnection) -> None:
    """Run migration synchronously.

    :param connection: Connection to use for the migration.
    """
    context.configure(
        # Pyright error: Argument of type "AsyncConnection" cannot be assigned
        # to parameter of type "Connection".
        connection=connection,  # type: ignore[reportGeneralTypeIssues]
        target_metadata=target_metadata,
        # Required as we are using a non-default schema.
        include_schemas=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    async with engine.connect() as connection:
        await connection.run_sync(_run_sync_migration)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
