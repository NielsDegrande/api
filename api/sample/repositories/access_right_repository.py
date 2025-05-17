"""Repository for access rights."""

from sqlalchemy.sql.expression import and_, select

from api.common.dto.user import User
from api.common.orm.users import Users
from api.sample.dto.access_right import ProductAccessRightResponse
from api.sample.orm.access_rights import ProductAccessRights
from api.utils.constants import AccessLevels
from api.utils.database import AsyncSessionLocal, orm_to_pydantic


async def create_access_right(
    product_id: int,
    user: User,
    access_level: AccessLevels,
) -> ProductAccessRightResponse:
    """Add an access right for a user.

    :param product_id: Target for access right.
    :param user: User to add for.
    :param access_level: Access right to grant.
    :return: Granted access right.
    """
    # Avoid duplicates by returning existing access right if it exists.
    if (
        existing_access_right := await _read_access_right(
            product_id=product_id,
            user_id=user.user_id,
        )
    ) and existing_access_right.access_level == access_level:
        return existing_access_right

    access_right_orm = ProductAccessRights(
        user_id=user.user_id,
        product_id=product_id,
        access_level=access_level,
    )

    async with AsyncSessionLocal() as session, session.begin():
        session.add(access_right_orm)
        await session.commit()
        access_right_orm.username = user.username
        return orm_to_pydantic(access_right_orm, ProductAccessRightResponse)


async def _read_access_right(
    product_id: int,
    user_id: int,
) -> ProductAccessRightResponse | None:
    """Get access right for user.

    :param product_id: Target for access right.
    :param user_id: User to add for.
    :return: Access right.
    """
    async with AsyncSessionLocal() as session, session.begin():
        query = (
            select(ProductAccessRights, Users.username)  # pyright: ignore[reportCallIssue]
            .join(Users)
            .where(
                and_(
                    ProductAccessRights.user_id == user_id,  # pyright: ignore[reportArgumentType]
                    ProductAccessRights.product_id == product_id,  # pyright: ignore[reportArgumentType]
                ),
            )
        )
        result = (await session.execute(query)).first()
        if result:
            access_right, user_name = result
            return ProductAccessRightResponse(
                access_right_id=access_right.access_right_id,
                user_id=access_right.user_id,
                username=user_name,
                product_id=access_right.product_id,
                access_level=access_right.access_right,
            )
        return None
