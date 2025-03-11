# We assume all encrypted secrets follow the naming pattern {{SECRET_DIR}}/*{{ENC_SUFFIX}}
set positional-arguments
set shell := ["bash", "-cue"]
root_dir := `git rev-parse --show-toplevel`
version := `git describe --tags --abbrev=0`
ctr := "docker"
image := "ghcr.io/sdsc-ordes/gimie-api:" + version
image_dir := root_dir + "/tools/image"

# Default recipe to list all recipes.
[private]
default:
  just --list image --no-aliases

# Build images
build *args:
  @echo "🐋 Building container image"
  cd {{root_dir}} && \
    {{ctr}} build \
      -f "{{image_dir}}/Dockerfile" \
      -t "{{image}}" \
      --build-arg VERSION="{{version}}" \
      {{args}} \
      .

# Run image
run *args: build
  cd {{root_dir}} && \
    {{ctr}} run \
      --env-file .env \
      -p 7123:15400 \
      {{args}} \
      "{{image}}"

# Push images
push *args: build
  @echo "🐋 Pushing container image"
  cd {{root_dir}} && \
    {{ctr}} push {{args}} {{image}}

# Start the compose stack
compose-up *args: 
  @echo "🐋 Running compose"
  cd {{root_dir}} && \
    {{ctr}} compose \
      --env-file .env \
      --project-directory "{{root_dir}}" \
      -f "{{image_dir}}/compose.yml" \
      up --build {{args}}

