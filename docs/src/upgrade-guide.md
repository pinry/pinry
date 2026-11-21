Pinry 3.0
=========

Pinry 3.0 is a rebuild on a current base. There is **no upgrade path from
2.x**: the database migrations start over, so a 2.x database can't be
migrated, and `local_settings.py` is no longer read. Start a fresh install
with [Install with Docker](install-with-docker.md).

# What changed

+ **Backend:** Django 5.2 LTS on Python 3.12 or newer (the Docker image uses
  Python 3.13). Dependencies are managed with uv and locked in `uv.lock`.
+ **Frontend:** Vue 3 with Vite, Buefy 3 and Bulma 1, built with Node 26 and
  pnpm.
+ **Docker:** the image is based on Debian 13 (trixie) and builds for
  `linux/amd64` and `linux/arm64`. 32-bit ARM is no longer supported. The
  image isn't published to a registry; build it from the repository. It has
  a health check, and gunicorn is only reachable through nginx.
+ **Configuration:** every setting is an environment variable, normally kept
  in `.env` (see `.env.example`). Pinry refuses to start in Docker without
  `SECRET_KEY` and `ALLOWED_HOSTS`.
+ **Databases:** SQLite (the default) and PostgreSQL 14 or newer, chosen with
  `DATABASE_URL`. MySQL and Oracle are no longer supported.
+ **API:** an OpenAPI 3 schema at `/api/v2/schema/` and Swagger UI at
  `/api/v2/docs/`, both served without any outside CDN. HTTP Basic auth is
  off unless `ALLOW_BASIC_AUTH=true`; use an API token instead. Pins, boards
  and public profiles no longer include anyone's `email`. See
  [API support](api.md).
+ **Security:** user-supplied text and links are escaped and limited to
  http(s); pinning by URL can't reach private addresses unless
  `ALLOW_PRIVATE_URL_FETCH=true`; failed logins are rate limited; private
  boards and pins stay hidden everywhere in the API.

# Moving pins from a 2.x install

There is no automatic import. If you need to keep pins from a 2.x install,
the API is the most practical route: read pins from the old instance with
its API and create them on the new one with an API token (`POST
/api/v2/pins/` with a `url`, or upload the file to `/api/v2/images/` first).
