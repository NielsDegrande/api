FROM python:3.14-slim AS base_bare

LABEL NAME=api
LABEL VERSION=1.0.0

WORKDIR /app

# Install uv by copying its static binary from the official distroless image.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install curl for the health check.
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml, uv.lock and README.md files.
COPY pyproject.toml uv.lock README.md ./
COPY api/__init__.py api/__init__.py

# Install dependencies.
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen

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

# Run the API as a non-root user.
RUN useradd --create-home api \
    && chown -R api:api /app
USER api


FROM base_bare AS test

# Dependencies for pre-commit and its hooks.
# Node-based hooks require libatomic1.
RUN apt-get update \
    && apt-get install --no-install-recommends -y git libatomic1 shellcheck \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies with dev and test extras.
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --group dev --group test
COPY .pre-commit-config.yaml .pre-commit-config.yaml

# Install pre-commit hooks.
RUN git init .
RUN pre-commit install-hooks
RUN git config --global --add safe.directory /app
