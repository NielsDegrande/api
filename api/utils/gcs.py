"""Utils to interact with GCS."""

import datetime
from functools import cache, lru_cache

from google.cloud.storage import Bucket, Client


@cache
def _get_bucket(bucket_name: str) -> Bucket:
    """Get bucket to interact with.

    :param bucket_name: Name of the GCS bucket.
    :return: Bucket to interact with.
    """
    client = Client()
    return client.get_bucket(bucket_name)


@lru_cache(maxsize=32)
def read_bytes(
    bucket_name: str,
    file_path: str,
) -> bytes:
    """Read bytes from GCS.

    :param bucket_name: Name of the GCS bucket.
    :param file_path: Path to bytes to read.
    :return: Content at file path.
    """
    blob = _get_bucket(bucket_name).blob(file_path)
    return blob.download_as_bytes()


def generate_download_signed_url_v4(
    bucket_name: str,
    blob_name: str,
    expiration_in_minutes: int,
) -> str:
    """Generate a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.

    :param bucket_name: Name of the bucket containing the blob to download.
    :param blob_name: Name of the blob to download.
    :param expiration_in_minutes: Expiration time of the signed URL, in minutes.
    :return: Download signed URL.
    """
    blob = _get_bucket(bucket_name).blob(blob_name)
    return blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes.
        expiration=datetime.timedelta(minutes=expiration_in_minutes),
        # Allow GET requests using this URL.
        method="GET",
    )
