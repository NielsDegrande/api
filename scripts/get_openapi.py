"""Get OpenAPI specification for this API."""

import json
from pathlib import Path

from fastapi.openapi.utils import get_openapi

from api.api import api

openapi_specification = get_openapi(
    title=api.title,
    version=api.version,
    openapi_version=api.openapi_version,
    summary=api.summary,
    description=api.description,
    routes=api.routes,
)

with Path("openapi.json").open("w") as file_:
    json.dump(openapi_specification, file_, indent=4)
