"""Repository for common database interactions using SQLModel."""

from typing import Any, Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.sql import text # For the standalone check_db function
from sqlmodel import SQLModel, select
# AsyncSession is imported by AsyncSessionLocal, but explicit import can be good for type hinting if needed directly.
# from sqlmodel.ext.asyncio.session import AsyncSession 

from api.utils.database import AsyncSessionLocal


# Define a TypeVar for the SQLModel model type
TypeVarModel = TypeVar("TypeVarModel", bound=SQLModel)
# Define a TypeVar for the Pydantic schema type used for updates/inputs if they differ from the model
TypeVarSchema = TypeVar("TypeVarSchema", bound=BaseModel)


async def check_db() -> None:
    """Run a simple query against the database. This is the original function."""
    async with AsyncSessionLocal() as session, session.begin(): # Ensure session.begin() if using SQLAlchemy < 2.0 style commit-as-you-go
        await session.execute(text("SELECT 1"))


class DefaultRepository(Generic[TypeVarModel, TypeVarSchema]):
    """Generic repository with common CRUD operations for SQLModel models."""

    def __init__(self, model: Type[TypeVarModel]):
        """
        Initialize the repository with a specific SQLModel model.

        :param model: The SQLModel model class.
        """
        self._model = model

    async def create(self, model_object: TypeVarModel) -> TypeVarModel:
        """
        Create a new record in the database.

        :param model_object: The SQLModel instance to create.
        :return: The created SQLModel instance with updated fields (e.g., ID).
        """
        async with AsyncSessionLocal() as session:
            session.add(model_object)
            await session.commit()
            await session.refresh(model_object)
            return model_object

    async def get_by_id(self, entity_id: Any) -> TypeVarModel | None:
        """
        Retrieve a record by its primary key.

        :param entity_id: The primary key of the record to retrieve.
        :return: The SQLModel instance if found, otherwise None.
        """
        async with AsyncSessionLocal() as session:
            return await session.get(self._model, entity_id)

    async def get_all(self) -> list[TypeVarModel]:
        """
        Retrieve all records of the model type.

        :return: A list of SQLModel instances.
        """
        async with AsyncSessionLocal() as session:
            statement = select(self._model)
            result = await session.exec(statement)
            return result.all()

    async def update(
        self, entity_id: Any, data_update: TypeVarSchema # TypeVarSchema for update data structure
    ) -> TypeVarModel | None:
        """
        Update an existing record in the database.

        :param entity_id: The primary key of the record to update.
        :param data_update: A Pydantic model instance containing the fields to update.
                             Assumes data_update is a Pydantic model (like a SQLModel schema without table=True).
        :return: The updated SQLModel instance if found and updated, otherwise None.
        """
        async with AsyncSessionLocal() as session:
            db_model = await session.get(self._model, entity_id)
            if db_model:
                # exclude_unset=True ensures only fields explicitly set in data_update are used.
                update_data = data_update.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(db_model, key, value)
                session.add(db_model)
                await session.commit()
                await session.refresh(db_model)
            return db_model

    async def delete(self, entity_id: Any) -> TypeVarModel | None:
        """
        Delete a record by its primary key.

        :param entity_id: The primary key of the record to delete.
        :return: The SQLModel instance that was deleted, if found, otherwise None.
        """
        async with AsyncSessionLocal() as session:
            db_model = await session.get(self._model, entity_id)
            if db_model:
                await session.delete(db_model)
                await session.commit()
            return db_model
