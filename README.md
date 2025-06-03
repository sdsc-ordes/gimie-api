# GimieAPI

Containerized REST API around [gimie](https://github.com/sdsc-ordes/gimie).

## Usage

### Setup

This repository contains a [justfile](./justfile), and we use [`just`](https://github.com/casey/just) as a command runner.

We provide all the tools you need to work on this project in a nix development shell.
See here to install nix: https://determinate.systems/nix-installer/

To enter the dev-shell, run:

```shell
just dev
```

> [!NOTE]
> Alternatively, you may enter the devshell directly with :
> `nix develop ./tools/nix#default --accept-flake-config --command "zsh"`


### With docker

We build two docker images, a small "headless" version with only the REST server, and a larger image that bundles the REST server and a streamlit web application. These two images are differentiated by their tag: `<version>` vs `<version>-webapp`.

First rename the `.env.dist` file to `.env` and add your github/gitlab token. Then you can run:

``` bash
just image compose-up
```

or

``` bash
just image build
just image run
```

### With docker compose

For development, it may be more convenient to use our docker compose stack.

```
just image compose-up
```

This will serve a container exposing the API on port 7123.


## How to use the API

Entry point to the API

``` bash
http://0.0.0.0:7123/
```

In case we want to obtain the gimie output in json, just add the repo link to `/gimie/jsonld/GITHUB_REPO`

``` bash
http://0.0.0.0:7123/gimie/jsonld/https://github.com/sdsc-ordes/gimie
```

To calculate the graph and provide a serialized output in ttl do `/gimie/project/GITHUB_REPO`

``` bash
http://0.0.0.0:7123/gimie/ttl/https://github.com/sdsc-ordes/gimie
```

## How to access to the API documentation 

``` bash
http://localhost:7123/docs
```

## Deployment

We provide manifests to deploy the service on kubernetes.
The manifest templates in [tools/deploy](tools/deploy) are managed with ytt and can be rendered using:

```shell
just manifests render
```

Or deployed directly with:

```shell
just manifests deploy
```
