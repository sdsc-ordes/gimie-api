set positional-arguments
set shell := ["bash", "-cue"]

root_dir := `git rev-parse --show-toplevel`


# Default recipe to list all recipes.
[private]
default:
    just --list --no-aliases

alias fmt := format
# Format manifests.
format *args:
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

alias dev := nix-develop
# Enter a Nix development shell.
nix-develop *args:
    @echo "Starting nix developer shell in './tools/nix/flake.nix'."
    @cd "{{root_dir}}" && \
    cmd=("$@") && \
    { [ -n "${cmd:-}" ] || cmd=("zsh"); } && \
    nix develop ./tools/nix#default --accept-flake-config --command "${cmd[@]}"

