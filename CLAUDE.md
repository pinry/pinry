# CLAUDE.md

This file guides Claude Code (claude.ai/code) when working in this repository.

## Fork and upstream

This repository is `octanewt/pinry`, a fork of `pinry/pinry` (upstream). Open pull requests against this fork's `master`. Don't open a pull request on `pinry/pinry`, or offer to, unless the user explicitly asks for one.

## Project overview

Pinry is a self-hosted, Pinterest-style image board. It has two parts:

- **Backend**: Django 5.2 LTS (`django>=5.2,<5.3`) with Django REST Framework, on Python 3.12+. It serves a JSON API under `/api/v2/` and the Django admin. Dependencies are managed with **uv** (`pyproject.toml`, `uv.lock`). CI and the Docker image install from `uv.lock`; there is no `requirements.txt`.
- **Frontend**: a Vue 3 single-page app in `pinry-spa/` (Buefy 3 on Bulma 1, vue-router 5, vue-i18n 11, @yeger/vue-masonry-wall, axios), written in JavaScript with the Options API. It is built with Vite and managed with **pnpm** 12 (`pnpm-lock.yaml`; `pnpm-workspace.yaml` lists which dependencies may run build scripts).

The backend does not render the app's pages; the SPA does all UI. In production (Docker), nginx serves `pinry-spa/dist` for `/`, serves `/static` and `/media` from `/data/static`, and proxies `/api` and `/admin` to gunicorn.

## Common commands

Backend (from the repo root, see `Makefile`):

```sh
uv sync                                     # make install
uv run python manage.py migrate             # make migrate
uv run python manage.py runserver           # make serve (binds 0.0.0.0:8000)
uv run python manage.py test                # make test, runs all Django tests
uv run python manage.py test core.tests.api.PinTests   # one test class
uv run flake8                               # make flake8
uv run python manage.py makemigrations      # make makemigrations
make lock                                   # uv lock after changing pyproject.toml
uv run python manage.py spectacular --validate --file schema.yml   # check the OpenAPI schema
uv run mkdocs serve                         # make docs-serve (docs in docs/src)
```

Frontend (from `pinry-spa/`, Node 26):

```sh
pnpm install
pnpm serve    # Vite dev server on :5173; proxies /api, /admin, /media, /static to 127.0.0.1:8000
pnpm build    # production build into pinry-spa/dist (CI runs this)
pnpm lint     # ESLint 10 flat config (eslint.config.js): eslint-plugin-vue + @stylistic
```

For local development, run `manage.py runserver` and `pnpm serve` at the same time.

CI (`.github/workflows/`) does the following:

- **Backend:** runs `uv sync --locked`, then flake8, `makemigrations --check` and the Django tests on Python 3.12, 3.13 and 3.14, all on SQLite. A second job runs the tests on PostgreSQL 17 (Python 3.13); tests that need concurrent write transactions, such as `core/tests/concurrency.py`, are skipped on SQLite.
- **Frontend:** runs `pnpm install --frozen-lockfile`, `pnpm lint` and `pnpm build` on Node 26.
- **Docker:** builds the release image and smoke-tests it, builds the dev image, and builds for arm64 (see Docker below).

Keep code compatible with Python 3.12 (the `requires-python` floor). When you change dependencies in `pyproject.toml`, run `make lock` and commit `uv.lock`; CI's `uv sync --locked` fails on a stale lock.

## Settings

- All site settings come from **environment variables**, read in `pinry/settings/base.py` through the helpers in `pinry/settings/env.py` and documented in `.env.example`. There is no `local_settings.py`. `DATABASE_URL` (parsed by dj-database-url) picks the database, SQLite by default.
- `manage.py` defaults to `pinry.settings.development` unless `DJANGO_SETTINGS_MODULE` or `--settings` is given. The development settings set `DEBUG=True`, fall back to a dummy `SECRET_KEY` and `ALLOWED_HOSTS=['*']`, and add `django_extensions`. `manage.py` also sets `settings.IS_TEST = True` whenever `test` is in argv, and when `IS_TEST` is true, `pinry/urls.py` also serves static files.
- `pinry/settings/base.py` holds the shared config, including `PUBLIC`, `ALLOW_NEW_REGISTRATIONS`, `IMAGE_SIZES`, `IMAGE_PATH`, `IMAGE_AUTO_DELETE` and the DRF config:
  - Authentication: Token and Session, plus Basic only when `ALLOW_BASIC_AUTH=True` (`users/auth/throttling.py`). Failed password checks are throttled per client address (`LoginRateThrottle`, rate `DEFAULT_THROTTLE_RATES["login"]`, env `LOGIN_THROTTLE_RATE`), enforced in `CombinedAuthBackend`.
  - Pagination: LimitOffset, with `PAGE_SIZE=50`.
  - `URL_FIELD_NAME="resource_link"`.
  - Schema: drf-spectacular (`DEFAULT_SCHEMA_CLASS`). The OpenAPI 3 schema is at `/api/v2/schema/` and Swagger UI at `/api/v2/docs/`. Custom filter backends describe their query parameters in `get_schema_operation_parameters`.
  - `DEFAULT_AUTO_FIELD` is `BigAutoField`.
- `pinry/settings/docker.py` is the production config. It is selected with `ENV DJANGO_SETTINGS_MODULE` in `Dockerfile.autobuild` and `_start_gunicorn.sh`, not with a `--settings` flag. It keeps the database (SQLite at `/data/production.db` unless `DATABASE_URL` is set), static files and media in `/data`, and refuses to start without `SECRET_KEY` and `ALLOWED_HOSTS`.
- Django 4+ requires a scheme in each `CSRF_TRUSTED_ORIGINS` value (`https://pins.example.com`); the system check rejects bare host names.

## Architecture

Django apps:

- **`core/`** holds the domain models `Pin`, `Board` and `Image` (`core.Image` subclasses `django_images.Image`). It also holds:
  - The DRF viewsets and router (`core/views.py`, `drf_router`), mounted at `/api/v2/`: `pins`, `images`, `boards`, `tags-auto-complete` and `boards-auto-complete`.
  - The serializers and the permissions (`IsOwnerOrReadOnly`, `OwnerOnlyIfPrivate`, ...).

  Details:
  - **Privacy**: private boards and pins are filtered for non-owners in `core/serializers.py` (`filter_private_pin`, `filter_private_board`) and in the viewset querysets. Any change to how pins or boards are listed must keep this filtering.
  - `Pin.url` and `Pin.referer` hold up to 2048 characters. `referer` is labelled "Source" in the UI.
  - Pins can share an image. `delete_pin_images` (`core/models.py`) deletes an image with its last pin, after locking the image row with `select_for_update()` so concurrent deletes can't leave it orphaned (issue #7).
  - `manage.py prune_images` lists, and with `--delete` deletes, images no pin uses that are older than `--older-than` hours (default 24), using `django_images.Image.created`. Abandoned uploads are the usual source. See `docs/src/install-with-docker.md`.
  - `manage.py import_pinterest <export.html> --user <name>` imports boards and pins from Pinterest's "Request your data" HTML export (`core/importers/`: `pinterest_export.py` parses only the Boards and Pins sections, `importer.py`'s `PinImporter` writes them). Images are fetched from `i.pinimg.com` through `create_for_url`; `Pin.source_id` (`pinterest:<pin id>`, unique per user) makes re-runs skip imported pins. Anything not clearly public is imported private. See `docs/src/import-pinterest.md`. Real exports contain personal data: never commit one; tests build a made-up page.
  - When an image is fetched from a URL, it is checked with Pillow (`ImageManager._is_valid_image`) and rejected if Pillow can't open it.
  - Tags use `django-taggit` 6 (`pin.tags.set(list)`, not `set(*tags)`). Filtering uses `django-filter`; viewsets declare `filterset_fields`/`filterset_class`.
  - Multi-tag search is in `core/filters.py` (`TagsFilterBackend`): `/api/v2/pins/?tags=a&tags=b&tags_mode=all|any`, defaulting to `all`. The frontend sends repeated `tags=` keys through `serializeParams` in `api.js`.
- **`django_images/`** is a vendored image library. It provides the base `Image` and `Thumbnail` models, MD5-hashed upload paths, and thumbnail generation at the sizes in `IMAGE_SIZES`. `Image.uploaded_by` is set on upload and URL fetch, and `ReusableImageField` lets only the uploader pin an image no pin uses yet (issue #6). `Image.save` records `Image.sha256` (of the bytes as received); uploads and URL pins reuse an existing image with the same hash only if it is in `reusable_images(request)` (`core/serializers.py`, the same set `ReusableImageField` accepts), so other users' private images are never reused (issue #8). `manage.py images_hash [--merge]` backfills hashes and merges same-user duplicates. `Image.created` records when the image was stored. Signal handlers delete files on disk when rows are deleted (`IMAGE_AUTO_DELETE`).
- **`users/`** has the custom `User` model, the login and logout views, and the `users` and `public-users` viewsets, mounted at `/api/v2/profile/`.
  - `users.auth.backends.CombinedAuthBackend` adds email login (emails aren't unique: it logs in only when exactly one account's password matches) and leaves usernames to `ModelBackend`. Registration runs `validate_password`. Logout is POST-only at `/api/v2/profile/logout/`.
  - `users.middleware.Public` returns 403 to anonymous requests when `PUBLIC=False`, except for `/api/v2/profile/` and `/admin/login/`. Requests with a valid token (or Basic auth, when enabled) pass too, since DRF only authenticates them later in the view.
  - **API tokens** (`rest_framework.authtoken`): a `post_save` signal creates a token for every user (`create_token_if_necessary`). `UserSerializer.get_token` returns it only when the requester is that user. `manage.py users_reset_tokens` deletes all tokens. Unauthenticated API requests get 401, not 403. See `docs/src/api.md`.
- **`pinry_plugins/`** is the plugin system.
  - Each class path in `settings.ENABLED_PLUGINS` is instantiated in `builder/_loader.py`.
  - `pre_save` signal handlers call the hooks `process_image_pre_creation` and `process_thumbnail_pre_creation` on new `core.Image` and `Thumbnail` rows, catching and logging any exception a plugin raises.
  - `batteries/plugin_example.py` shows the interface. See `docs/src/plugin-system.md`.
- **`pinry/`** is the project package: settings, root `urls.py`, and `middleware.py` (`ForceCSRFCookieMiddleware`, which makes sure the SPA gets a CSRF cookie). It also contains the bookmarklet, `pinry/static/js/bookmarklet.js`.

Frontend (`pinry-spa/src/`):

- `components/api.js` is the single API client. It wraps axios calls to `/api/v2/` in objects such as `Board`, `Pin`, `User` and `Tag`. Add new backend calls here instead of calling axios from components.
- `router/index.js` defines the routes, which map to `views/` (`Pins4Board`, `Pins4Tag`, `Pins4User`, `Profile4User`, `Search`, ...). Reusable UI lives in `components/`:
  - Editors and modals are under `components/editors/` and `components/pin_edit/`.
  - The profile and API-token UI is in `components/user/`.
- **i18n**: user-facing strings go through vue-i18n (`$t(...)`, composition mode with global injection). The locale files are `components/utils/i18n/locales/{en,zh,fr}.json`, registered in `components/utils/i18n/index.js`, which also exports `setLocale`. When you add a string, add its key to `en.json` at minimum, and to the other locales when you can. The chosen language is saved in local storage.
- **Vue 3 specifics**:
  - Modals open through `components/modals.js` (`$buefy.modal.open`). A modal's component closes itself with `$emit('close')` and declares its events in `emits`; the `events` option maps to its listeners.
  - Cross-component refreshes go through the mitt bus in `components/utils/bus.js` (`bus.bus.on/off/emit`). Remove listeners and the scroll handler in `beforeUnmount`.
  - Pin and board grids use `MasonryWall`, which only notices a new `items` array: assign a new array, never push into it.
  - Only the Buefy components registered in `main.js` are available; register a new one there before using it.
  - **Theme**: light, dark or system (the default, which follows the OS). `public/theme-init.js` sets `data-theme` on `<html>` before the app loads, and `components/utils/theme.js` (`setTheme`, the navbar switch) changes it; the choice is saved in local storage under `theme`. Bulma themes its own components. Pinry's own styles use the `--pinry-*` CSS variables in `components/utils/theme.scss`, never hard-coded colours, so both themes work. The pin preview modal is dark in both themes on purpose.

## Tests

- Backend tests live in `core/tests/` (`api.py` and `views.py`, re-exported from `core/tests/__init__.py`, so register new test modules there), `users/tests.py`, `django_images/tests.py` and `pinry_plugins/tests.py`.
- Use the fixture helpers in `core/tests/helpers.py` (`create_user`, `create_image`, `create_pin`, `create_tag`). Their test image is `docs/src/imgs/logo-dark.png`, so that file must stay where it is.
- API tests use DRF's `APITestCase`.
- Image files are deleted on commit (`transaction.on_commit` in `django_images/models.py`), so inside a `TestCase` wrap the delete in `self.captureOnCommitCallbacks(execute=True)` to check that files are gone. `manage.py test` gives each run a temporary `MEDIA_ROOT`.
- To run the tests on PostgreSQL locally, set `DATABASE_URL=postgres://...` (the test runner creates its own `test_` database).
- The frontend has no test suite. `pnpm lint` and `pnpm build` are the checks.

## Conventions

- flake8 config is in `.flake8`: max line length 80, but E501 is ignored. Migrations, `pinry/settings/` and `core/tests/` are excluded. Bugbear (`B`) checks are selected.
- flake8-bugbear is installed, so the `B` checks run (B950 is ignored, like E501). No formatter is enforced; match the style of the surrounding code.
- Tests use `unittest.mock`.
- After changing models, generate migrations with `manage.py makemigrations` and commit them. Don't hand-edit existing migrations. The migration history was reset for 3.0 (no upgrade path from 2.x databases).
- Frontend code follows airbnb-like rules, enforced by ESLint (2-space indent, semicolons, single quotes, trailing commas).
- User-supplied text and URLs are untrusted. Render text with `{{ }}`, or through `niceLinks` (`components/utils/niceLinks.js`, which escapes everything) when it needs `v-html`. Pass any user-supplied `href` through `safeUrl` (`components/utils/safeUrl.js`), which allows only http(s). The API also rejects non-http(s) `url` and `referer` values (`validate_http_url` in `core/serializers.py`). Never cache the API token in localStorage.

## Docker

- `Dockerfile.autobuild` builds the release image on `python:3.13-slim-trixie`, for linux/amd64 and linux/arm64 (no 32-bit ARM). It is a single image with nginx, gunicorn and the built SPA. The SPA stage runs on the build platform (`node:26-trixie-slim`); the Python stage installs `uv.lock` into `/opt/venv`. It has a `HEALTHCHECK` (`docker/scripts/healthcheck.py`).
- Configure the container with environment variables (`.env.example`). `docker-compose.example.yml` (SQLite, LAN) and `docker-compose.postgres.example.yml` (PostgreSQL 17, behind a TLS proxy) read `.env`.
- `Dockerfile` and `docker-compose.dev.yml` are for development: runserver and the Vite dev server with the source mounted (`make dev-docker-serve`).
- The image is not published to a registry (user's choice, 2026-10-23); everyone builds it locally. `docker/build_docker.sh` (or `make docker-build`) tags `pinry:local`, which the compose examples use. Runtime scripts are in `docker/scripts/` (`start.sh`, `_start_gunicorn.sh`, `gen_key.sh`, `healthcheck.py`), and the nginx config, which sends `X-Frame-Options: sameorigin`, is in `docker/nginx/`. gunicorn listens on 127.0.0.1:8000 only; nginx is the way in.
- CI (`.github/workflows/docker.yml`) builds the amd64 image and runs `docker/tests/smoke.sh` on it (`make docker-smoke-test` locally), builds the dev image, and builds the arm64 image under QEMU.
- Persistent data (the database, static files and media) lives in the `/data` volume. `start.sh` chowns `/data` to `www-data` (uid 1000) on every start.
