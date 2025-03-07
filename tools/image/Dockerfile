FROM python:3.12-slim-bookworm
ARG VERSION="latest"

EXPOSE 15400

# Metadata
LABEL org.opencontainers.image.source=https://github.com/sdsc-ordes/gimie-api
LABEL org.opencontainers.image.licenses=AGPL-3.0
LABEL org.opencontainers.image.title="Gimie API"
LABEL org.opencontainers.image.description="API for extracting RDF metadata from git repositories."
LABEL org.opencontainers.image.version=${VERSION}

# install uv
COPY --from=ghcr.io/astral-sh/uv:0.6.3 /uv /uvx /bin/

# install git
RUN apt-get update && apt-get install -y git && apt-get clean

ADD src CHANGELOG LICENSE README.md pyproject.toml uv.lock /app
WORKDIR /app
RUN uv sync --frozen

ENTRYPOINT ["uv", "run", "uvicorn", "src.gimie-api.main:app", "--host", "0.0.0.0", "--port", "15400"]
