# Developing Pinry

Pinry currently has two major requirements:

- Python@3.12+
- NodeJS@26

For minor requirements you need two have installed two package managers that
are not the defaults for these languages:

- Python, uv
- NodeJS, pnpm

To install these is pretty simple, you can just run:

    cd pinry
    pip install uv    # or see https://docs.astral.sh/uv/
    npm install -g pnpm@12

After that you can install this project with:

    uv sync
    cd pinry-spa; pnpm install

You will need to run two separate items as of right now, the SPA and the
backend:

    uv run python manage.py migrate
    uv run python manage.py runserver

And from another terminal:

    cd pinry-spa; pnpm serve

The SPA is built with Vite. Its dev server runs on http://localhost:5173 and
proxies `/api`, `/admin`, `/media` and `/static` to the Django server on
port 8000. Before sending a change, run `pnpm lint` and `pnpm build` in
`pinry-spa`, which is what CI runs.


## Testing

We have many tests built into Pinry to ensure that changes don't break
anything. If you are live dangerously and have cutting edge new Pinry
features first you can use our master branch for your own instance. We
recommend using our tags/versions though.

To run Pinry's tests inside the Pinry repo run:

    uv run python manage.py test

# Docker

You can also develop inside Docker, without installing Python or Node
locally. You need Docker with the Compose plugin.

    make dev-docker-serve    # docker compose -f docker-compose.dev.yml up --build

This mounts the repository into the containers and runs the Django dev
server on port 8000 and the Vite dev server on http://localhost:5173, both
reloading as you edit. The development settings are used, so no `.env` is
needed. Run commands inside it with, for example:

    docker compose -f docker-compose.dev.yml exec web uv run python manage.py createsuperuser

To build and check the release image as CI does:

    make docker-build          # tags pinry:local
    make docker-smoke-test     # builds, then runs docker/tests/smoke.sh

See [Install with Docker](install-with-docker.md) for running it.
