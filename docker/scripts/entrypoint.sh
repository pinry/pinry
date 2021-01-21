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
PROJECT_ROOT="/pinry"

mkdir -p /data/pinry-spa
cp -R /pinry/pinry-spa/dist /data/pinry-spa/

cd ${PROJECT_ROOT} || exit 1
python manage.py collectstatic --noinput --settings=pinry.settings.docker
python manage.py migrate --noinput --settings=pinry.settings.docker

exec "$@"
