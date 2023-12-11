"""Common API endpoints."""

from fastapi import APIRouter

from api.common.services import default_service
from api.utils.constants import ApplicationTags

common_router = APIRouter(tags=[ApplicationTags.COMMON])


@common_router.get("/")
@common_router.get("")
async def api_root() -> None:
    """Get the root of the API."""


@common_router.get("/auth")
async def authenticate() -> None:
    """Authenticate."""


@common_router.get("/db")
async def check_db() -> None:
    """Check if the database is responding."""
    return await default_service.check_db()


@common_router.get("/file")
async def download_file(
    file_path: str,
) -> str:
    """Generate temporary download links to files on a set bucket.

    :param file_path: Path to file to download.
    :return: File content.
    """
    return await default_service.download_file(file_path=file_path)
