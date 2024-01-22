"""File to store global constants.

Do not put constants related to an individual part of the app here.
"""

from enum import StrEnum

# Extensions.
YAML_EXTENSION = ".yaml"


# FastAPI tags.
class ApplicationTags(StrEnum):
    """Tags for FastAPI."""

    COMMON = "common"
    SAMPLE = "sample"
