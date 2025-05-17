"""Base ORM."""

from sqlmodel import SQLModel

# Use SQLModel as the declarative base for all ORM models.
Base = SQLModel
