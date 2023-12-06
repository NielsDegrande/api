"""File to store global constants.

Do not put constants related to an individual part of the app here.
"""

from enum import StrEnum


# FastAPI tags.
class ApplicationTags(StrEnum):
    """Tags for FastAPI."""

    COMMON = "common"
    SAMPLE = "sample"
