# Recipes for rendering and deploying manifests to a Kubernetes cluster.
# Secrets are loaded from the .env file at the root of the project.
root_dir := `git rev-parse --show-toplevel`
deploy_dir := root_dir + "/tools/deploy"
set positional-arguments
set shell := ["bash", "-cue"]
# Secrets from YTT prefixed env vars to inject into manifests.
export YTT_tokens__github := env('GITHUB_TOKEN')
export YTT_tokens__gitlab := env('GITLAB_TOKEN')

# Default recipe to list all recipes.
[private]
default:
  just --list manifests --no-aliases

# Render manifests
render: 
  cd "{{deploy_dir}}/ytt" && \
    ytt \
      --data-values-env YTT \
      -f common.lib.star \
      -f templates/ \
      -f schema.yaml

alias apply := deploy
# Apply manifests to the cluster.
deploy:
  just manifests render \
    | kubectl apply -f-
