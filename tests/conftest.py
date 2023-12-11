"""Configure tests."""

import base64

import pytest
from box import Box
from fastapi.testclient import TestClient

from api.api import api
from api.utils.config import load_config
from configs import CONFIGS_DIRECTORY

USERNAME = "user"
PASSWORD = "password"  # noqa: S105


@pytest.fixture(scope="session")
def config() -> Box:
    """Get test configuration.

    :return: Test configuration.
    """
    config_path = CONFIGS_DIRECTORY / "test.yaml"
    return load_config([config_path])


@pytest.fixture(scope="session")
def test_client() -> TestClient:
    """Get a test client.

    :return: Test client for API.
    """
    return TestClient(api)


@pytest.fixture(scope="session")
def basic_auth_header() -> str:
    """Create basic authentication header.

    :return: Basic authentication header.
    """
    user_pass = f"{USERNAME}:{PASSWORD}"
    user_pass_b64 = base64.b64encode(user_pass.encode()).decode()
    return f"Basic {user_pass_b64}"
