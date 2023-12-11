#!/bin/sh

# Start API.
uvicorn api.api:api --host 0.0.0.0 --port 80 --workers 4
