#!/bin/bash
gunicorn pinry.wsgi \
         --access-logfile '-' \
         --capture-output \
         --error-logfile '-' \
         --timeout 30 \
         -b 0.0.0.0:8000 \
         -w 4
