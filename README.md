# GimieAPI

## How to build this docker container

First rename the `.env.dist` file to `.env` and add your github/gitlab token. Then you can run:

``` bash
make docker-compose-up
```

or

``` bash
make docker-build
make docker-run
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
