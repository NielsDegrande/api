FROM python:3.12 AS base_bare

LABEL NAME=api
LABEL VERSION=1.0.0

WORKDIR /app

# Install poetry, do this before copying files for caching purposes.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir poetry==1.8.2

# Copy pyproject.toml, poetry.lock and README.md files.
COPY pyproject.toml poetry.lock README.md ./
COPY api/__init__.py api/__init__.py

# Install dependencies.
RUN poetry config virtualenvs.create false && poetry install --no-cache

# Expose the server.
EXPOSE 80

# Add a health check for the service.
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=3 \
    CMD curl --fail http://localhost:80/api/docs || exit 1

ENTRYPOINT [ "bash" ]

FROM base_bare AS base

ENTRYPOINT ["bash", "scripts/start.sh"]

# Copy all other files here to optimize caching.
COPY ./ ./

FROM base_bare AS test

# Dependencies for pre-commit.
RUN apt-get update \
    && apt-get install shellcheck -y \
    && apt-get clean

# Install poetry dependencies with dev and test extras.
RUN poetry install --no-cache --with dev,test
COPY .pre-commit-config.yaml .pre-commit-config.yaml

# Install pre-commit hooks.
RUN git init . && pre-commit install-hooks
RUN git config --global --add safe.directory /app
