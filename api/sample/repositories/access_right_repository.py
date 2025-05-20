"""Repository for access rights using SQLModel."""

from pydantic import BaseModel
from sqlmodel import select, SQLModel # SQLModel is also a Pydantic BaseModel

from api.common.orm.users import Users # Needed for relationship access
from api.sample.orm.access_rights import ProductAccessRights # SQLModel ORM class
from api.common.repositories.default_repository import DefaultRepository
from api.utils.constants import AccessLevels
from api.utils.database import AsyncSessionLocal


# Pydantic schema for creating product access rights
class ProductAccessRightsCreateSchema(BaseModel):
    product_id: int
    user_id: int # Changed from User DTO to user_id directly for simplicity in schema
    access_level: AccessLevels


# Pydantic schema for updating product access rights
class ProductAccessRightsUpdateSchema(BaseModel):
    access_level: AccessLevels | None = None


class ProductAccessRightsRepository(
    DefaultRepository[ProductAccessRights, ProductAccessRightsUpdateSchema]
):
    """
    Repository for managing product access rights.
    """

    def __init__(self) -> None:
        """Initialize the product access rights repository."""
        super().__init__(ProductAccessRights)

    async def get_by_product_and_user(
        self, product_id: int, user_id: int
    ) -> ProductAccessRights | None:
        """
        Get a specific access right by product ID and user ID.

        :param product_id: ID of the product.
        :param user_id: ID of the user.
        :return: ProductAccessRights ORM instance or None.
        """
        async with AsyncSessionLocal() as session:
            statement = (
                select(ProductAccessRights)
                .where(ProductAccessRights.product_id == product_id)
                .where(ProductAccessRights.user_id == user_id)
            )
            result = await session.exec(statement)
            return result.first()
            # Note: Accessing result.user.username for response transformation
            # would happen in a service layer, potentially requiring a session.

    async def create_access_right(
        self, access_right_data: ProductAccessRightsCreateSchema
    ) -> ProductAccessRights:
        """
        Create an access right for a user and product.
        Avoids duplicates: returns existing if same access level already present.

        :param access_right_data: Data for creating the access right.
        :return: Created or existing ProductAccessRights ORM instance.
        """
        existing_access_right = await self.get_by_product_and_user(
            product_id=access_right_data.product_id,
            user_id=access_right_data.user_id,
        )

        if (
            existing_access_right
            and existing_access_right.access_level == access_right_data.access_level
        ):
            return existing_access_right

        # If it exists but access level is different, the DefaultRepository.update would be used.
        # This custom create method specifically handles "create or return existing if identical".
        # For "create or update if different", the service layer would call get_by_product_and_user,
        # then either this create_access_right (if None) or repo.update (if different level).

        access_right_orm = ProductAccessRights(
            user_id=access_right_data.user_id,
            product_id=access_right_data.product_id,
            access_level=access_right_data.access_level,
        )
        # Use the inherited create method from DefaultRepository
        return await self.create(access_right_orm)

    # The following methods are inherited from DefaultRepository and available:
    # - async def create(self, model_object: ProductAccessRights) -> ProductAccessRights:
    # - async def get_by_id(self, entity_id: Any) -> ProductAccessRights | None: (PK for ProductAccessRights is access_right_id)
    # - async def get_all(self) -> list[ProductAccessRights]:
    # - async def update(self, entity_id: Any, data_update: ProductAccessRightsUpdateSchema) -> ProductAccessRights | None:
    # - async def delete(self, entity_id: Any) -> ProductAccessRights | None:

# The original _read_access_right's logic of joining with Users to fetch username
# for a ProductAccessRightResponse DTO is now simplified. The repository returns the
# ORM model. The service layer would be responsible for constructing any specific DTOs,
# which might involve accessing related model fields (e.g., access_right_instance.user.username).
# The original create_access_right function's responsibility is now split:
# - Data validation/DTO input: Handled by ProductAccessRightsCreateSchema.
# - Core creation: Handled by DefaultRepository.create.
# - Duplicate check & specific creation logic: Handled by ProductAccessRightsRepository.create_access_right.
# The orm_to_pydantic conversion is no longer needed.
# The direct setting of `access_right_orm.username = user.username` is removed as `username` is not a field of ProductAccessRights.
# This information would be derived from the related User object in the service layer if needed for a response DTO.
