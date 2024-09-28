"""File to store global constants.

Do not put constants related to an individual part of the app here.
"""

from enum import StrEnum, auto

# Extensions.
YAML_EXTENSION = ".yaml"


# FastAPI tags.
class ApplicationTag(StrEnum):
    """Tags for FastAPI."""

    COMMON = auto()
    SAMPLE = auto()
