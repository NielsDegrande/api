"""Configure tests."""

import base64

import pytest
from box import Box
from httpx import ASGITransport, AsyncClient

from api.api import api
from api.utils.config import load_config
from api.utils.constants import YAML_EXTENSION
from configs import CONFIGS_DIRECTORY

USERNAME = "user"
PASSWORD = "password"  # noqa: S105 - Possible hardcoded password.


@pytest.fixture(scope="session")
def config() -> Box:
    """Get test configuration.

    :return: Test configuration.
    """
    config_path = CONFIGS_DIRECTORY / f"test{YAML_EXTENSION}"
    return load_config([config_path])


@pytest.fixture
def async_client() -> AsyncClient:
    """Get an async test client.

    :return: Async client for API.
    """
    return AsyncClient(
        # Pyright error: Argument of type "FastAPI" cannot be assigned
        # to parameter of type "_ASGIApp".
        transport=ASGITransport(app=api),  # type: ignore[reportArgumentType]
        base_url="http://localhost:8080",
    )


@pytest.fixture(scope="session")
def auth_header() -> dict[str, str]:
    """Create basic authentication header.

    :return: Basic authentication header.
    """
    user_pass = f"{USERNAME}:{PASSWORD}"
    user_pass_b64 = base64.b64encode(user_pass.encode()).decode()
    return {"Authorization": f"Basic {user_pass_b64}"}
