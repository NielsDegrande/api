#!/usr/bin/make

## help: Print help.
.PHONY: help
help:
	@echo Possible commands:
	@cat Makefile | grep '##' | grep -v "Makefile" | sed -e 's/^##/  -/'

## install: Install dependencies.
.PHONY: install
install:
	uv sync --no-dev

## install_dev: Install dependencies for development.
.PHONY: install_dev
install_dev:
	uv sync --group dev --group test
	# Installs the pre-commit hook.
	. .venv/bin/activate && pre-commit install

## build_base_bare: Build the base image without any dependencies.
.PHONY: build_base_bare
build_base_bare:
	docker build \
		--file Dockerfile \
		--target base_bare \
		--tag api-bare \
		--cache-from=api-bare \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		${PWD}

## build_base: Build the base image.
.PHONY: build_base
build_base:
	docker build \
		--file Dockerfile \
		--target base \
		--tag api \
		--cache-from=api-bare \
		--cache-from=api \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		${PWD}

## build_base_amd: Build the base image for AMD64 architecture.
.PHONY: build_base_amd
build_base_amd:
	docker build \
		--file Dockerfile \
		--target base \
		--tag api_amd \
		--cache-from=api-bare \
		--cache-from=api \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		--platform linux/amd64 \
		${PWD}

## build_test: Build the test image.
.PHONY: build_test
build_test:
	docker build \
		--file Dockerfile \
		--target test \
		--tag api-test  \
		--cache-from=api-bare \
		--cache-from=api \
		--cache-from=api-test \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		${PWD}

## run_pre_commit: Run pre-commit.
.PHONY: run_pre_commit
run_pre_commit: build_test
	docker run --rm \
		--volume ${PWD}:/app \
		api-test \
		-c "pre-commit run --all-files"

## run_tests: Run tests.
.PHONY: run_tests
run_tests: build_test
	cd tests; docker-compose up --exit-code-from api

## run_container: Run container.
.PHONY: run_container
run_container: build_test
	docker run -it --rm \
		--volume ${PWD}/:/app/ \
		api-test

## generate_openapi: Generate OpenAPI specification.
.PHONY: generate_openapi
generate_openapi:
	python scripts/get_openapi.py
