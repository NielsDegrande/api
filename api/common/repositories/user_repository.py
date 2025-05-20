"""User repository using SQLModel."""

from pydantic import BaseModel, Field as PydanticField
from sqlmodel import select, SQLModel # SQLModel is also a Pydantic BaseModel

from api.common.orm.users import Users # SQLModel ORM class
from api.common.repositories.default_repository import DefaultRepository
from api.utils.database import AsyncSessionLocal


# Pydantic schema for creating a user
class UserCreateSchema(BaseModel):
    username: str
    password_hash: str # In a real app, this would be just 'password' and hashing happens in service
    roles: str | None = None


# Pydantic schema for updating a user
class UserUpdateSchema(BaseModel):
    # Username is typically not updatable or handled very carefully
    # username: str | None = None 
    password_hash: str | None = None # For password changes
    roles: str | None = None
    # is_active, is_verified, is_superuser could be here if they were on the Users model


class UserRepository(DefaultRepository[Users, UserUpdateSchema]):
    """
    Repository for managing user records.
    Uses Users as the ORM model and UserUpdateSchema for update operations.
    """

    def __init__(self) -> None:
        """Initialize the user repository."""
        super().__init__(Users)

    async def get_by_username(self, username: str) -> Users | None:
        """
        Get a user by their username.

        :param username: Username to search for.
        :return: Matching Users ORM instance or None.
        """
        async with AsyncSessionLocal() as session:
            statement = select(Users).where(Users.username == username)
            result = await session.exec(statement)
            # HTTPException should be raised in the service/API layer, not repository.
            # Repository returns data or None.
            return result.first()

    async def create_user_from_schema(self, user_data: UserCreateSchema) -> Users:
        """
        Create a new user record from schema data.
        Note: Password hashing should ideally occur in the service layer before this.

        :param user_data: The user data from the DTO/schema.
        :return: The created Users ORM instance.
        """
        user_orm = Users(
            username=user_data.username,
            password_hash=user_data.password_hash, # Assumes password_hash is provided directly
            roles=user_data.roles,
        )
        # Use the inherited create method
        return await self.create(user_orm)

# Example of how it might be used (e.g., in a service layer):
# user_repo = UserRepository()
# user_to_find = await user_repo.get_by_username("john_doe")
# if not user_to_find:
#     new_user_dto = UserCreateSchema(username="john_doe", password_hash="hashed_password", roles="user")
#     created_user = await user_repo.create_user_from_schema(new_user_dto)
# else:
#     update_dto = UserUpdateSchema(roles="admin")
#     updated_user = await user_repo.update(entity_id=user_to_find.user_id, data_update=update_dto)

# The original read_user function is now replaced by UserRepository.get_by_username.
# The HTTPException logic has been removed from the repository method; it should be
# handled by the caller (e.g., service layer or API endpoint) based on the None return value.
# The orm_to_pydantic conversion is no longer needed.
