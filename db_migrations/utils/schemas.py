"""Util functions for database migration."""

from alembic import op


def create_schema(schema_name: str) -> None:
    """Create a schema if it does not exist.

    :param schema_name: Name of the schema.
    """
    op.execute(f"""CREATE SCHEMA IF NOT EXISTS {schema_name};""")


def drop_schema(schema_name: str) -> None:
    """Drop all tables in schema and delete the schema.

    :param schema_name: Name of the schema.
    """
    op.execute(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;")
