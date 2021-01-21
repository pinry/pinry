#!/bin/bash
gunicorn pinry.wsgi \
         --access-logfile '-' \
         --capture-output \
         --error-logfile '-' \
         --timeout 30 \
         -b "0.0.0.0:${APP_PORT}" \
         -w 4
