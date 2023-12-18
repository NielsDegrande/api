"""Pydantic model for a user."""

from pydantic import BaseModel


class User(BaseModel):
    """Pydantic model for a user."""

    user_id: int
    username: str
    password_hash: str
    roles: str
