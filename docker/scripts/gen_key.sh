#!/bin/bash
# Print a new random SECRET_KEY, for example:
#   docker run --rm pinry:local /pinry/docker/scripts/gen_key.sh
exec python -c "import secrets; print(secrets.token_urlsafe(50))"
