"""Database utilities."""

import sys
from typing import TypeVar

from box import Box
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import (
    # "async_sessionmaker" is unknown import symbol.
    async_sessionmaker,  # pyright: ignore[reportAttributeAccessIssue]
    create_async_engine,
)
from sqlalchemy.pool import (
    AsyncAdaptedQueuePool,
    NullPool,
)
from sqlmodel import SQLModel

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
    poolclass=NullPool if "pytest" in sys.modules else AsyncAdaptedQueuePool,
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    # Require explicit refreshes for performance reasons.
    expire_on_commit=False,
)


TypeVarBaseModel = TypeVar("TypeVarBaseModel", bound=BaseModel)
# Pyright warning: Variable not allowed in type expression.
TypeVarORMModel = TypeVar(
    "TypeVarORMModel",
    bound=SQLModel,  # pyright: ignore[reportInvalidTypeForm]
)


def orm_to_pydantic(
    # Pyright warning: TypeVar appears only once in generic function signature.
    orm_object: TypeVarORMModel,  # pyright: ignore[reportInvalidTypeVarUse]
    pydantic_class: type[TypeVarBaseModel],
) -> TypeVarBaseModel:
    """Convert an ORM object to a Pydantic object.

    :param orm_object: ORM object to convert.
    :param pydantic_class: Pydantic class of the resulting object.
    :return: A valid Pydantic object.
    """
    return pydantic_class.model_validate(orm_object, from_attributes=True)


def pydantic_to_orm(
    pydantic_object: BaseModel,
    orm_class: type[TypeVarORMModel],
) -> TypeVarORMModel:
    """Convert a Pydantic object to an ORM object.

    :param pydantic_object: Pydantic object to convert.
    :param orm_class: ORM class of the resulting object.
    :return: Converted ORM object.
    """
    return orm_class(**pydantic_object.model_dump())
