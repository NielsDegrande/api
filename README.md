# API

## Introduction

This repository holds the API.

## Getting Started

### Installation

```shell
python3 -m venv venv
source venv/bin/activate
make install_dev
```

If you want to commit changes to `/scripts/`,
you need to install ShellCheck, e.g. with:

```shell
brew install shellcheck
```

### Configure Environment Variables

```shell
# Database Configuration.
echo 'DB_DIALECT=postgresql' >> .env
echo 'DB_HOST=localhost' >> .env
echo 'DB_PORT=5432' >> .env
echo 'DB_NAME=db' >> .env
echo 'DB_USER=postgres' >> .env
echo 'DB_PASSWORD=password' >> .env

# Google Cloud Storage (GCS).
echo 'GCS_BUCKET_NAME=bucket' >> .env
```

### Database Setup

Start the database:

```shell
docker compose up -d
```

Ensure the database is up-to-date with the latest schemas and tables:

```shell
alembic upgrade head
```

Then populate the database. E.g., from the `Pipelines` repository.

### Start the API

Launch the API:

```shell
# Adding `--debug` will refresh the API upon code changes.
api --debug
```

## Security

### Authentication

Authentication is done with basic authentication.
This needs to be replaced by a more secure mechanism for any real world usage.

### Authorization

Authorization with a role-based access control (RBAC) system is currently not implemented.

### File Server

To share a file hosted on GCS, the API uses signed URLs.
This means that the API will generate a URL that is only valid for a limited time.
One needs to be authenticated to generate a signed URL.
This should not be used for confidential documents.
