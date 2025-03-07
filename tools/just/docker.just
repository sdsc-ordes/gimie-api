# We assume all encrypted secrets follow the naming pattern {{SECRET_DIR}}/*{{ENC_SUFFIX}}
set positional-arguments
set shell := ["bash", "-cue"]
root_dir := `git rev-parse --show-toplevel`
ctr := "docker"
tag := "latest"
image := "ghcr.io/sdsc-ordes/gimie-api:" + tag
image_dir := root_dir + "/tools/image/Dockerfile"

# Default recipe to list all recipes.
[private]
default:
  just --list docker --no-aliases

# Build Docker images
build:
  @echo "🐋 Building docker image"
  cd {{root_dir}} && \
    {{ctr}} build \
      -f "{{image_dir}}" \
      -t "{{image}}" \
      --build-arg VERSION="{{tag}}" \
      .
# Run docker image
run: build
  cd {{root_dir}} && \
    {{ctr}} run \
      --env-file .env \
      -p 7123:15400 \
      "{{image}}"

# Push Docker images
push: build
  @echo "🐋 Pushing docker image"
  cd {{root_dir}} && \
    {{ctr}} push {{image}}

compose-up: ## Run the Docker Compose stack
  @echo "🐋 Running docker-compose"
  cd {{root_dir}} && \
    {{ctr}} compose \
      -f "{{image_dir}}" \
      up --build

