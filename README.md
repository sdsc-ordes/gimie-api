# GimieAPI

## How to build this docker container

First rename the `.env.dist` file to `.env` and add your github/gitlab token. Then you can run:

```
docker-compose up # add -d for detached
```

This will serve a instance running by default in port 7123. 

### How to restart the docker container.

```
docker restart gimieapi
docker image rm -f gimieapi-core_api
```

## How to use the API

Entry point to the API
```
http://0.0.0.0:7123/
```

In case we want to obtain the gimie output in json, just add the repo link to `/gimie/jsonld/GITHUB_REPO`

```
http://0.0.0.0:7123/gimie/jsonld/https://github.com/SDSC-ORD/gimie
```

To calculate the graph and provide a serialized output in ttl do `/gimie/project/GITHUB_REPO`

```
http://0.0.0.0:7123/gimie/ttl/https://github.com/SDSC-ORD/gimie
```

## How to access to the API documentation 

```
http://localhost:8000/docs
```

## ChangeLog

- v0.0.2: Updating gimie to release  [0.6.0 release](https://github.com/SDSC-ORD/gimie/releases/tag/0.6.0).
- v0.0.1: Basic service using main branch from gimie. 