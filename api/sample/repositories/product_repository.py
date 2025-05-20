"""Products repository using SQLModel."""

from sqlmodel import select, SQLModel
from sqlalchemy.sql.expression import Select // For type hinting if constructing complex selects

from api.sample.orm.products import Products # SQLModel ORM
from api.sample.orm.access_rights import ProductAccessRights # SQLModel ORM
from api.common.repositories.default_repository import DefaultRepository
from api.utils.constants import AccessLevels
from api.utils.database import AsyncSessionLocal # Renamed to avoid conflict with session instance

# Assuming these DTOs are Pydantic models. If not, they'd need to be defined/converted.
from api.sample.dto.product import ProductRequest as ProductCreateSchema
from api.sample.dto.product import ProductUpdate as ProductUpdateSchema
# ProductResponse DTO would be used by the service layer after getting Products model.


class ProductRepository(DefaultRepository[Products, ProductUpdateSchema]):
    """
    Repository for managing products with access control.
    Inherits basic CRUD from DefaultRepository and adds custom methods for access-controlled operations.
    """

    def __init__(self) -> None:
        """Initialize the product repository."""
        super().__init__(Products)

    async def create_product_from_schema(self, product_data: ProductCreateSchema) -> Products:
        """
        Create a new product from schema data.
        This method assumes that product_data is a Pydantic model (e.g., ProductRequest).

        :param product_data: Data for creating the product (e.g., name, color, price).
        :return: The created Products ORM instance.
        """
        # The field names in ProductCreateSchema must match the arguments for Products model
        product_orm = Products(**product_data.model_dump())
        return await self.create(product_orm) # Uses DefaultRepository.create

    async def list_products_for_user(self, user_id: int) -> list[Products]:
        """
        Read products accessible by a specific user.

        :param user_id: ID of the user requesting the products.
        :return: List of accessible Products ORM instances.
        """
        async with AsyncSessionLocal() as session:
            statement = (
                select(Products)
                .join(ProductAccessRights, Products.product_id == ProductAccessRights.product_id)
                .where(ProductAccessRights.user_id == user_id)
            )
            result = await session.exec(statement)
            return result.all()

    async def _get_product_for_user_with_access_check(
        self,
        session: AsyncSessionLocal, # Type hint for the session instance
        user_id: int,
        product_id: int,
        access_levels: list[AccessLevels] | None = None,
        with_for_update: bool = False,
    ) -> Products | None:
        """
        Private helper to read a product by ID for a user, checking access levels.
        Returns the Products ORM instance or None.
        """
        statement: Select = ( # Explicitly type 'statement' for clarity
            select(Products)
            .join(ProductAccessRights, Products.product_id == ProductAccessRights.product_id)
            .where(ProductAccessRights.user_id == user_id)
            .where(Products.product_id == product_id)
        )
        if access_levels:
            statement = statement.where(ProductAccessRights.access_level.in_(access_levels))
        
        if with_for_update:
            # Applying FOR UPDATE to the Products table in the context of this join
            statement = statement.with_for_update(of=Products)

        result = await session.exec(statement)
        return result.first()

    async def get_product_for_user(
        self, user_id: int, product_id: int, access_levels: list[AccessLevels] | None = None
    ) -> Products | None:
        """
        Read a specific product by ID for a user, optionally checking access levels.

        :param user_id: ID of the user requesting the product.
        :param product_id: ID of the product to read.
        :param access_levels: Optional list of access levels required.
        :return: Matching Products ORM instance or None. Repository should not raise HTTPExceptions.
        """
        async with AsyncSessionLocal() as session:
            product = await self._get_product_for_user_with_access_check(
                session=session,
                user_id=user_id,
                product_id=product_id,
                access_levels=access_levels,
            )
            return product

    async def update_product_for_user(
        self,
        user_id: int,
        product_id: int,
        product_update_data: ProductUpdateSchema,
    ) -> Products | None:
        """
        Update a product for a user, checking 'MANAGE' or 'WRITE' access.
        Repository should not raise HTTPExceptions.

        :param user_id: ID of the user updating the product.
        :param product_id: ID of the product to update.
        :param product_update_data: Data to update the product with (Pydantic model).
        :return: Updated Products ORM instance or None if not found or no access.
        """
        async with AsyncSessionLocal() as session:
            product_to_update = await self._get_product_for_user_with_access_check(
                session=session,
                user_id=user_id,
                product_id=product_id,
                access_levels=[AccessLevels.MANAGE, AccessLevels.WRITE],
                with_for_update=True, 
            )

            if not product_to_update:
                return None 

            update_data = product_update_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(product_to_update, key, value)
            
            session.add(product_to_update)
            await session.commit()
            await session.refresh(product_to_update)
            return product_to_update

    async def delete_product_for_user(
        self,
        user_id: int,
        product_id: int,
    ) -> Products | None:
        """
        Delete a product for a user, checking 'MANAGE' access.
        Repository should not raise HTTPExceptions.

        :param user_id: ID of the user deleting the product.
        :param product_id: ID of the product to delete.
        :return: The deleted Products ORM instance or None if not found or no access.
        """
        async with AsyncSessionLocal() as session:
            product_to_delete = await self._get_product_for_user_with_access_check(
                session=session,
                user_id=user_id,
                product_id=product_id,
                access_levels=[AccessLevels.MANAGE],
            )

            if not product_to_delete:
                return None
            
            await session.delete(product_to_delete)
            await session.commit()
            return product_to_delete
