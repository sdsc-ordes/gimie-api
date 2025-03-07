# We assume all encrypted secrets follow the naming pattern {{SECRET_DIR}}/*{{ENC_SUFFIX}}
root_dir := `git rev-parse --show-toplevel`
deploy_dir := root_dir + "/tools/deploy"
set shell := ["bash", "-cue"]

# Default recipe to list all recipes.
[private]
default:
  just --list manifests --no-aliases

alias fmt := format
# Format manifests.
format:
  @cd "{{deploy_dir}}" && \
    ytt fmt -f .

# Render manifests
render: 
  cd "{{deploy_dir}}" && \
    ytt \
      -f common.lib.star \
      -f k8s/ \
      -f schema.yaml

alias apply := deploy
# Apply manifests to the cluster.
deploy:
  just manifests render \
    | kubectl apply -f-
