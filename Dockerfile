# Development image: Python with uv, and Node with pnpm. The source is
# mounted at /app by docker-compose.dev.yml; nothing is copied in.
FROM node:26-trixie-slim AS node

FROM python:3.13-slim-trixie

COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
# node needs libatomic, which the node image has and the Python one lacks.
RUN apt-get update \
 && apt-get -y install --no-install-recommends libatomic1 \
 && rm -rf /var/lib/apt/lists/* \
 && ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
 && npm install -g pnpm@12 \
 && pip install --no-cache-dir uv

# Keep the virtualenv out of the mounted source tree.
ENV UV_PROJECT_ENVIRONMENT=/venv \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

WORKDIR /app
