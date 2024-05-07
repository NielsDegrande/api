#!/bin/bash

# Stop upon error and undefined variables.
# Print commands before executing.
set -eux

# Upgrade the database.
alembic upgrade head

# Add test user.
python scripts/add_test_user.py

# Start API as background process and capture process ID.
chmod +x /app/scripts/start.sh
/app/scripts/start.sh &
PID=$!

# Request the API main page.
sleep 10
CODE=$(curl -o /dev/null --silent --get --write-out '%{http_code}\n' -u user:password localhost:80/api)
if test "$CODE" -eq 200; then
    echo "API is responding"
else
    echo "API encountered error"
    exit 1
fi

# Kill the API process.
kill $PID

# Run tests.
pytest -n auto -rf --durations=0 tests

# Destroy the database.
alembic downgrade base
