#!/bin/sh

# Install curl.
apk add curl

# Request the API main page.
CODE=$(curl -o /dev/null --silent --get --write-out '%{http_code}\n' api:80/api)

if test "$CODE" -eq 200
then
	echo "API is responding"
    exit 0
else
	echo "API encountered error"
    exit 1
fi
