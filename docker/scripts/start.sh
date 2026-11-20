#!/bin/bash
# -----------------------------------------------------------------------------
# docker-pinry start script
#
# Collects static files, applies migrations, then runs nginx and gunicorn.
# Stops at the first error, e.g. a missing SECRET_KEY or ALLOWED_HOSTS.
# -----------------------------------------------------------------------------
set -e

cd /pinry

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# The data volume may come from the host with other owners. A full chown -R
# walks every file, which takes minutes on large volumes and on slow bind
# mounts (Docker Desktop on Windows/macOS), so it runs only when /data or an
# entry directly inside it is not owned by www-data. Fix deeper files by hand:
#   docker compose exec pinry chown -R www-data:www-data /data
if [ -n "$(find /data -maxdepth 1 \( ! -user www-data -o ! -group www-data \) -print -quit)" ]; then
    echo "Fixing ownership of /data (this can take a while)..."
    chown -R www-data:www-data /data
fi

/usr/sbin/nginx

exec ./docker/scripts/_start_gunicorn.sh
