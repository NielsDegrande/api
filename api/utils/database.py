"""Database utilities."""

from contextlib import contextmanager
from functools import cache
from typing import Generator, TypeVar

from box import Box
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from api.common.orm.base import Base
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


@cache
def _get_session_factory() -> sessionmaker:
    """Create a session factory.

    :return: SQLAlchemy session factory.
    """
    engine = create_engine(create_connection_string())
    return sessionmaker(bind=engine)


@contextmanager
def database_session() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations.

    :yield: Newly created SQLAlchemy session.
    """
    factory = _get_session_factory()
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


TypeVarBaseModel = TypeVar("TypeVarBaseModel", bound=BaseModel)
TypeVarORMModel = TypeVar("TypeVarORMModel", bound=Base)


def orm_to_pydantic(
    orm_object: TypeVarORMModel,
    pydantic_class: type[TypeVarBaseModel],
) -> TypeVarBaseModel:
    """Convert an ORM object to a Pydantic object.

    :param orm_object: the ORM object to convert.
    :param pydantic_class: the Pydantic class of the resulting object.
    :return: the Pydantic object.
    """
    return pydantic_class.model_validate(orm_object, from_attributes=True)


def pydantic_to_orm(
    pydantic_object: BaseModel,
    orm_class: type[TypeVarORMModel],
) -> TypeVarORMModel:
    """Convert a Pydantic object to an ORM object.

    :param pydantic_object: the Pydantic object to convert.
    :param orm_class: the ORM class of the resulting object.
    :return: the ORM object.
    """
    return orm_class(**pydantic_object.model_dump())
