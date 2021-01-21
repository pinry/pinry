#!/bin/sh

envsubst '${APP_HOST} ${APP_PORT}' < /etc/nginx/pinry.conf.template > /etc/nginx/sites-enabled/pinry.conf

exec "$@"
