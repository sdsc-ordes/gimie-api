FROM python:3.12-slim-bookworm
ARG VERSION="latest"

EXPOSE 15400
COPY --from=ghcr.io/astral-sh/uv:0.6.3 /uv /uvx /bin/

# Metadata
LABEL org.opencontainers.image.source=https://github.com/sdsc-ordes/gimie-api
LABEL org.opencontainers.image.licenses=AGPL-3.0
LABEL org.opencontainers.image.title="Gimie API"
LABEL org.opencontainers.image.description="API for extracting RDF metadata from git repositories."
LABEL org.opencontainers.image.version=${VERSION}


ADD . /app
WORKDIR /app
RUN uv sync --frozen

ENTRYPOINT ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]
