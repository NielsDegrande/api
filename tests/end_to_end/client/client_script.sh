#!/bin/sh

# Install curl.
apk add curl

# Request the API main page.
CODE=$(curl -o /dev/null --silent --get --write-out '%{http_code}\n' api:80/api)

# Due to authentication, the API should return 401.
# While not a success code, it indicates the API is responding.
if test "$CODE" -eq 401; then
    echo "API is responding"
    exit 0
else
    echo "API encountered error"
    exit 1
fi
