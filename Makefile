VERSION = latest
IMAGE = ghcr.io/sdsc-ordes/gimie-api
CONTAINER_RUNTIME ?= docker

.PHONY: docker-build
docker-build: ## Build Docker images
	@echo "🐋 Building docker image"
	$(CONTAINER_RUNTIME) build \
		-f tools/docker/Dockerfile \
		-t $(IMAGE):$(VERSION) \
		--build-arg VERSION=$(VERSION) \
		.

.PHONY: docker-run
docker-run: docker-build ## Run docker image
	$(CONTAINER_RUNTIME) run \
		--env-file .env \
		-p 7123:15400 \
		$(IMAGE):$(VERSION)

.PHONY: docker-push
docker-push: docker-build ## Push Docker images
	@echo "🐋 Pushing docker image"
	$(CONTAINER_RUNTIME) push $(IMAGE):$(VERSION)

docker-compose-up: ## Run the Docker Compose stack
	@echo "🐋 Running docker-compose"
	$(CONTAINER_RUNTIME) compose \
		-f tools/docker/compose.yml \
		up --build

.PHONY: format
format: install ## Format python code
	ruff format src

.PHONY: lint
lint: install ## Lint python code
	ruff check src

.PHONY: install
install: ## Setup project for development
	pip install -e '.[test,dev]'


.PHONY: test
test: install ## Run unit tests
	pytest

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
