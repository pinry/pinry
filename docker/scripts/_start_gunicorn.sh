#!/bin/bash
gunicorn pinry.wsgi -b 0.0.0.0:8000 -w 4 \
    --capture-output --timeout 30 --user www-data --group www-data