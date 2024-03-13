"""Main object of the API."""

import logging
import os
import traceback
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from api.common.controllers.default_controller import common_router
from api.common.controllers.feedback_controller import feedback_router
from api.common.services.user_service import authorize_user
from api.sample.controllers.product_controller import product_router
from api.utils.constants import ApplicationTag
from ui import UI_DIRECTORY

log_ = logging.getLogger(__name__)

tags_metadata = [
    {
        "name": ApplicationTag.COMMON,
        "description": "Default and shared operations.",
    },
    {
        "name": ApplicationTag.SAMPLE,
        "description": "Operations for the sample part of the application.",
    },
]

api = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    openapi_tags=tags_metadata,
    redoc_url=None,
    title="API",
    description="API to support web application.",
    version="0.0.1",
    dependencies=[
        Depends(authorize_user),
    ],
)


api.add_middleware(  # CORS
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.exception_handler(Exception)
async def exception_handler(request: Request, error: Exception) -> JSONResponse:
    """Handle all other exceptions raised by API.

    :param request: Request that triggered the exception
    :param error: Exception raised by application
    :return: Response to client
    """
    log_.exception(error)
    content = {
        "message": "Something went wrong.",
        "url": str(request.url),
        "sender": str(request.client),
        "exception_args": [repr(x) for x in error.args],
        "trace": traceback.format_exc().split("\n"),
    }
    return JSONResponse(
        status_code=500,
        content=content,
    )


# Add the default API routes.
api.include_router(common_router, prefix="/api")
api.include_router(feedback_router, prefix="/api")
# Add sample routes.
api.include_router(product_router, prefix="/api/sample")


@api.get("/api/{full_path:path}", include_in_schema=False)
async def catch_api_all() -> FileResponse:
    """Return 404 for non-existent api endpoints.

    :return: When we reach this part of the routing precedence, return 404.
    """
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@api.get("/{full_path:path}", include_in_schema=False)
async def catch_all(request: Request) -> FileResponse:
    """Serve the index.html as a template.

    :param request: Request received by API.
    :return: When we reach this part of the routing precedence, return index.html.
    """
    ui_directory_path = Path(UI_DIRECTORY)
    relative_file_path = request.path_params["full_path"]
    file_path = ui_directory_path / relative_file_path

    # Avoid path traversal attacks by checking we are inside folder.
    if os.path.commonpath([ui_directory_path, file_path]) != UI_DIRECTORY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if Path.is_file(file_path):
        return FileResponse(file_path)

    return FileResponse(ui_directory_path / "index.html")
