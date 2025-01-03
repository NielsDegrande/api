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

If you want to commit changes to `scripts`,
you need to install ShellCheck, e.g. with:

```shell
brew install shellcheck
```

### Configure Environment Variables

Copy the `.env.example` file to `.env` and fill in the values.

```shell
cp .env.example .env
```

### Database Setup

Start the database:

```shell
docker compose up -d
```

Upon API startup the database will be automatically migrated.
It can be done manually using:

```shell
alembic upgrade head
```

Then populate the database. E.g., from the `Pipelines` repository.
You need to add a user to the database with `python scripts/add_test_user.py`.

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

Authorization with a role-based access control (RBAC) system.

### File Server

To share a file hosted on GCS, the API uses signed URLs.
This means that the API will generate a URL that is only valid for a limited time.
One needs to be authenticated to generate a signed URL.
This should not be used for confidential documents.
