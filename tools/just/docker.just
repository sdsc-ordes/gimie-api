# We assume all encrypted secrets follow the naming pattern {{SECRET_DIR}}/*{{ENC_SUFFIX}}
root_dir := `git rev-parse --show-toplevel`
tag := "latest"
image := "ghcr.io/sdsc-ordes/gimie-api"
container_runtime := "docker"
set shell := ["bash", "-cue"]

# Default recipe to list all recipes.
[private]
default:
    just --list secrets --no-aliases

# Build Docker images
build:
	@echo "🐋 Building docker image"
  cd {{root_dir}} && \
    {{container_runtime}} build \
      -f "{{root_dir}}/tools/docker/Dockerfile" \
      -t "{{image}}:{{tag}}" \
      --build-arg VERSION="{{tag}}" \
      .
# Run docker image
run: build
  cd {{root_dir}} && \
	  {{container_runtime}} run \
      --env-file .env \
      -p 7123:15400 \
      $(IMAGE):$(VERSION)

# Push Docker images
push: build
	@echo "🐋 Pushing docker image"
  cd {{root_dir}} && \
	  {{container_runtime}} push {{image}}:{{tag}}

compose-up: ## Run the Docker Compose stack
	@echo "🐋 Running docker-compose"
  cd {{root_dir}} && \
    {{CONTAINER_RUNTIME}} compose \
      -f tools/docker/compose.yml \
      up --build

