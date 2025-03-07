# We assume all encrypted secrets follow the naming pattern {{SECRET_DIR}}/*{{ENC_SUFFIX}}
root_dir := `git rev-parse --show-toplevel`
DEPLOY_DIR := "{{root_dir}}/tools/deploy"
set shell := ["bash", "-cue"]

# Default recipe to list all recipes.
[private]
default:
    just --list secrets --no-aliases

alias fmt := format
# Format manifests.
format:
    @cd "{{root_dir}}" && \
    yamlfmt **/*.y{a,}ml

# Render manifests
render: 
  cd "{{root_dir}}/tools/deploy" && \
    ytt -f k8s/ -f schema.yaml -f values.yaml 

alias apply := deploy
# Apply manifests to the cluster.
deploy:
   just render | kubectl apply -
