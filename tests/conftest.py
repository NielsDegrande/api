"""Configure tests."""

import base64

import pytest
from box import Box
from httpx import AsyncClient

from api.api import api
from api.utils.config import load_config
from configs import CONFIGS_DIRECTORY

USERNAME = "user"
PASSWORD = "password"  # noqa: S105 - Possible hardcoded password.


@pytest.fixture(scope="session")
def config() -> Box:
    """Get test configuration.

    :return: Test configuration.
    """
    config_path = CONFIGS_DIRECTORY / "test.yaml"
    return load_config([config_path])


@pytest.fixture()
def async_client() -> AsyncClient:
    """Get an async test client.

    :return: Async client for API.
    """
    return AsyncClient(app=api, base_url="http://localhost:8080")


@pytest.fixture(scope="session")
def basic_auth_header() -> str:
    """Create basic authentication header.

    :return: Basic authentication header.
    """
    user_pass = f"{USERNAME}:{PASSWORD}"
    user_pass_b64 = base64.b64encode(user_pass.encode()).decode()
    return f"Basic {user_pass_b64}"
