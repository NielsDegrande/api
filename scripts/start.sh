#!/bin/bash

# Start API.
echo Upgrading database.
alembic upgrade head
echo Starting API.
uvicorn api.api:api --host 0.0.0.0 --port 80 --workers 4
