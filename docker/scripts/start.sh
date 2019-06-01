#!/bin/bash
# -----------------------------------------------------------------------------
# docker-pinry /start script
#
# Will setup database and static files if they don't exist already, if they do
# just continues to run docker-pinry.
#
# Authors: Isaac Bythewood
# Updated: Aug 19th, 2014
# -----------------------------------------------------------------------------


# If static files don't exist collect them
if [ ! -d /data/static ]
then
    cd /srv/www/pinry
    python manage.py collectstatic --noinput
fi

# If database doesn't exist yet create it
if [ ! -f /data/production.db ]
then
    cd /srv/www/pinry
    python manage.py migrate --noinput --settings=pinry.settings.docker
fi

# Fix all settings after all commands are run
chown -R www-data:www-data /data

# start all process
/usr/sbin/nginx

cd /srv/www/pinry/
/scripts/_start_gunicorn.sh
