Install with Docker
===================

Pinry runs as a single container: nginx serves the app and your images, and
gunicorn runs the Django API behind it. Everything you need to keep (the
SQLite database, static files and uploaded images) lives in the `/data`
volume.

The image is not published to a registry. You build it from this repository,
which takes a few minutes the first time. It builds for `linux/amd64` and
`linux/arm64` (for example a Raspberry Pi 4 or 5 running a 64-bit OS);
32-bit ARM is not supported.

You need Docker with the Compose plugin (`docker compose`, not the old
`docker-compose`).


# Quick start (home network, SQLite)

```
git clone https://github.com/octanewt/pinry
cd pinry
cp .env.example .env
cp docker-compose.example.yml docker-compose.yml
```

Edit `.env` and set the two required values:

```
SECRET_KEY=<paste the output of the command below>
ALLOWED_HOSTS=localhost,pinry.local,192.168.1.10
```

Generate the key with:

```
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

`ALLOWED_HOSTS` lists every host name and address you will type into the
browser to reach Pinry, comma separated. Requests for any other host get
`400 Bad Request`. Keep `localhost` if you open Pinry in a browser on the
machine that runs it. After changing `.env`, run `docker compose up -d` to
recreate the container; a plain restart keeps the old values.

Then build and start it, and create your admin account:

```
docker compose up -d --build
docker compose exec pinry python manage.py createsuperuser
```

Open `http://192.168.1.10/` (or whatever host you listed). The container
reports `healthy` in `docker compose ps` once nginx and the API both answer.

The database, static files and images are in `./data` next to the compose
file.


# On a server, behind HTTPS (PostgreSQL)

`docker-compose.postgres.example.yml` runs Pinry with PostgreSQL 17. Pinry
listens on `127.0.0.1:8080` only, so a TLS proxy on the same host (Caddy,
nginx, Traefik, ...) is the only way in.

```
cp .env.example .env
cp docker-compose.postgres.example.yml docker-compose.yml
```

In `.env`, set:

```
SECRET_KEY=<generated as above>
ALLOWED_HOSTS=pins.example.com
POSTGRES_PASSWORD=<another long random value>
HTTPS=true
```

Then start it the same way:

```
docker compose up -d --build
docker compose exec pinry python manage.py createsuperuser
```

Point your proxy at `http://127.0.0.1:8080`. It must pass the original
`Host` header and set `X-Forwarded-Proto: https`. With Caddy that is all
`reverse_proxy` needs:

```
pins.example.com {
    reverse_proxy 127.0.0.1:8080
}
```

With nginx:

```
location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    client_max_body_size 50M;
}
```

PostgreSQL keeps its data in `./postgres-data`, and Pinry keeps its images in
`./data`.

Once HTTPS works, you can also set `HSTS_SECONDS=31536000` so browsers stop
using plain HTTP for your site.


# Without Compose

```
./docker/build_docker.sh        # or: make docker-build
docker run -d --name pinry -p 80:80 \
    --env-file .env \
    -v "$(pwd)/data:/data" \
    --restart unless-stopped \
    pinry:local
```

`build_docker.sh` tags the image `pinry:local`, and also with the latest git
tag if there is one.


# Settings

All settings are environment variables, normally kept in `.env`. Restart the
container after changing them (`docker compose up -d`). `.env.example` lists
them all with their defaults.

**Required**

+ `SECRET_KEY`: a long random value. Keep it secret and keep it the same
  across restarts, or everyone is logged out. Pinry refuses to start without
  it.
+ `ALLOWED_HOSTS`: comma separated host names and addresses Pinry is reached
  at, e.g. `pins.example.com,192.168.1.10`. Pinry refuses to start without
  it.

**Database**

+ `DATABASE_URL`: defaults to SQLite at `/data/production.db`. For
  PostgreSQL 14 or newer use
  `postgres://user:password@host:5432/dbname`. MySQL and Oracle are not
  supported.
+ `POSTGRES_PASSWORD`: only used by `docker-compose.postgres.example.yml`,
  which builds `DATABASE_URL` from it.

**HTTPS and proxies**

+ `HTTPS=true`: set this when a proxy serves Pinry over HTTPS and sets
  `X-Forwarded-Proto`. Login and CSRF cookies are then sent over HTTPS only.
  Leave it unset for plain HTTP, or logins stop working.
+ `HSTS_SECONDS`: how long browsers should refuse plain HTTP for your site.
  Defaults to `0` (off). Set it only once HTTPS works, because browsers
  remember it.
+ `CSRF_TRUSTED_ORIGINS`: comma separated origins, with scheme (for example
  `https://pins.example.com`), that may log in when a proxy changes the host
  or scheme. Usually not needed.

**Who can see and join**

+ `PUBLIC`: defaults to `true`. Set it to `false` so that anonymous visitors
  see nothing; API clients with a token still work.
+ `ALLOW_NEW_REGISTRATIONS`: defaults to `true`. Set it to `false` once
  everyone has an account, and create further accounts with
  `createsuperuser` or in the admin at `/admin/`.

**Logins and the API**

+ `ALLOW_BASIC_AUTH`: defaults to `false`. Accept HTTP Basic auth on the API
  (`curl -u user:password`). API tokens are the better choice for scripts;
  see [API support](api.md).
+ `LOGIN_THROTTLE_RATE`: failed password checks allowed per client address,
  `20/hour` by default, or `off`.

**Pinning images by URL**

When you pin by URL, the server downloads the image itself. To stop users
from reaching internal services this way, Pinry refuses URLs that point to
loopback, private (LAN), link-local and other non-public addresses, follows
at most 3 redirects (each one checked the same way), and stops downloads that
are larger than the size limit or take longer than 20 seconds.

+ `ALLOW_PRIVATE_URL_FETCH`: defaults to `false`. Set it to `true` to pin
  images from hosts on your LAN. Only do this if you trust every account
  holder.
+ `MAX_FETCH_BYTES`: the largest image downloaded by URL, 50 MB by default.
  This matches the 50 MB upload limit in the bundled nginx config.

**Images**

+ `IMAGE_AUTO_DELETE`: defaults to `true`. Delete an image's files when no
  pin uses it any more.
+ `IMAGE_SIZES`: the thumbnail sizes, as JSON. See `.env.example` for the
  default.

**Plugins**

+ `ENABLED_PLUGINS`: comma separated plugin classes to load. See
  [Plugin System](plugin-system.md).


# Images are public

Image files under `/media` are served by nginx without a login check, even
with `PUBLIC=false` or on private boards. Anyone who has an image's URL can
open it. The URLs contain a hash, so they are hard to guess, but don't rely
on Pinry to keep the images themselves secret.


# Duplicate images

When you pin or upload a file that is identical to an image you can already
see (your own pins and uploads, and other people's public pins), Pinry reuses
the stored image instead of saving another copy. Images on other people's
private pins are never reused, so pinning a file doesn't tell you whether
someone else has it. Only byte-for-byte identical files match: the same
picture at another size or quality is stored separately.

Images stored before this was added (or restored from an old backup) have no
recorded hash. To fill it in and see how many duplicates there are:

    docker compose exec pinry python manage.py images_hash

Add `--merge` to fold duplicates whose pins all belong to the same user into
one image, deleting the extra copies. Images shared by several users' pins
and uploads no pin uses yet are left alone. Back up `./data` first.


# Updating

```
git pull
docker compose up -d --build
```

The container applies new database migrations every time it starts.


# Backup

Stop the container and copy `./data` (and `./postgres-data`, or better a
`pg_dump`, if you use PostgreSQL) somewhere safe:

```
docker compose stop
tar czf pinry-backup.tar.gz data
docker compose start
```

Keep a copy of `.env` too, since it holds your `SECRET_KEY`.


# Cleaning up unused images

When you upload an image and then close the new-pin dialog without saving, the
image stays in `./data` with no pin. `prune_images` finds images that no pin
uses and that were stored more than 24 hours ago, so an upload that is still
being pinned is left alone. On its own it only counts them; add `--delete` to
delete them:

```
docker compose exec pinry python manage.py prune_images
docker compose exec pinry python manage.py prune_images --delete
```

`--older-than HOURS` changes the 24 hour grace period, and `--verbosity 2`
lists each image. To run it regularly, add the `--delete` line to the host's
crontab. If `IMAGE_AUTO_DELETE` is off, the files stay on disk and only the
database rows are removed.


# Troubleshooting

+ **The container exits right away.** Run `docker compose logs pinry`. The
  usual cause is a missing `SECRET_KEY` or `ALLOWED_HOSTS`, and the log says
  which.
+ **`400 Bad Request` in the browser, or logging in does nothing.** The host
  name or address in the address bar is not in `ALLOWED_HOSTS`. Run
  `docker compose logs pinry | grep HTTP_HOST` to see the rejected host,
  and `docker compose exec pinry printenv ALLOWED_HOSTS` to see what the
  running container has. Add the host to `.env`, then
  `docker compose up -d`.
+ **Logging in fails with a CSRF error behind a proxy.** Check that the proxy
  passes `Host` and `X-Forwarded-Proto`, that `HTTPS=true` is set, and, if
  the proxy changes the host name, add the public origin to
  `CSRF_TRUSTED_ORIGINS`.
+ **Pinning a LAN image by URL fails.** That is the default; see
  `ALLOW_PRIVATE_URL_FETCH` above.
+ **Permission errors in `./data`.** The container runs as uid 1000 and
  changes the owner of `/data` to that user on every start.


# Why nginx is inside the container

gunicorn and Django are not built to serve static files and images, so the
image includes nginx to do that and passes only `/api` and `/admin` to
gunicorn. gunicorn listens on `127.0.0.1` inside the container, so nginx is
the only way to reach it.
