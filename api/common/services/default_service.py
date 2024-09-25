"""Service for common functionality."""

from fastapi import HTTPException, status

from api.common.repositories import default_repository
from api.config import config
from api.utils.gcs import generate_download_signed_url_v4


async def check_db() -> None:
    """Check if the database is responding."""
    try:
        await default_repository.check_db()
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database is not responding: {exception}",
        ) from exception


async def download_file(
    file_path: str,
    bucket_name: str = config.gcs.bucket_name,
    expiration_in_minutes: int = config.gcs.expiration_in_minutes,
) -> str:
    """Download file.

    :param file_path: Path to file to download.
    :param bucket_name: Name of the bucket to download from.
    :param expiration_in_minutes: Number of minutes until the download link expires.
    :return: Download link.
    """
    file_path = file_path.strip()
    return generate_download_signed_url_v4(
        bucket_name=bucket_name,
        blob_name=file_path,
        expiration_in_minutes=expiration_in_minutes,
    )
