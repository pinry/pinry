#!/bin/bash
exec gunicorn pinry.wsgi -b 127.0.0.1:8000 -w 4 \
    --capture-output --timeout 30 \
    --user www-data --group www-data \
    --env DJANGO_SETTINGS_MODULE=pinry.settings.docker
