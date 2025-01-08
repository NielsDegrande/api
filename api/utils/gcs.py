"""Utils to interact with GCS."""

import logging
from pathlib import Path

import aiofiles
import aiohttp
from async_lru import alru_cache
from gcloud.aio.storage import Storage

log_ = logging.getLogger(__name__)


# NOTE: Validate if you want caching here.
@alru_cache(maxsize=32)
async def read_bytes(bucket_name: str, file_path: str) -> bytes:
    """Read bytes from GCS asynchronously.

    :param bucket_name: Name of the GCS bucket.
    :param file_path: Path to bytes to read.
    :return: Content at file path.
    """
    async with Storage() as client:
        return await client.download(
            bucket_name,
            file_path,
        )


async def upload_bytes(
    source_file_path: Path,
    bucket_name: str,
    object_name: str,
) -> None:
    """Upload bytes to GCS asynchronously.

    :param source_file_path: Path to bytes to read.
    :param bucket_name: Name of the GCS bucket.
    :param object_name: Name of the object to create.
    """
    async with aiohttp.ClientSession() as session:
        client = Storage(session=session)

        async with aiofiles.open(source_file_path) as file_:
            output = await file_.read()
            status = await client.upload(
                bucket_name,
                object_name,
                output,
            )
            log_.info("Upload status: %s", status)


async def get_signed_url(
    bucket_name: str,
    blob_name: str,
    expiration_in_minutes: int,
) -> str:
    """Get signed URL for downloading a blob asynchronously.

    Note that this method requires a service account key file.
    You can not use this if you are using Application Default Credentials
    from Google Compute Engine or from the Google Cloud SDK.

    :param bucket_name: Name of the bucket containing the blob to download.
    :param blob_name: Name of the blob to download.
    :param expiration_in_minutes: Expiration time of the signed URL, in minutes.
    :return: Download signed URL.
    """
    storage = Storage()
    bucket = storage.get_bucket(bucket_name)
    blob = await bucket.get_blob(blob_name)
    return await blob.get_signed_url(expiration=expiration_in_minutes * 60)
