#!/bin/bash
# Smoke test for the release image: ./docker/tests/smoke.sh IMAGE
#
# Checks that the image refuses to start without its required settings,
# serves the SPA, API, docs, admin and static files, and keeps an uploaded
# pin across a restart. Run it from the repository root.
set -euo pipefail

IMAGE="${1:-pinry:ci}"
PORT="${PORT:-8080}"
NAME="pinry-smoke-$$"
BASE="http://localhost:${PORT}"
DATA="$(mktemp -d)"
SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')"

cleanup() {
    docker rm -f "$NAME" > /dev/null 2>&1 || true
}
trap cleanup EXIT

fail() {
    echo "FAIL: $*" >&2
    docker logs "$NAME" >&2 || true
    exit 1
}

expect() {
    local want="$1"; shift
    local got
    got="$(curl -s -o /dev/null -w '%{http_code}' "$@")"
    [ "$got" = "$want" ] || fail "$* answered $got, expected $want"
    echo "ok: $* -> $got"
}

wait_healthy() {
    for _ in $(seq 1 60); do
        case "$(docker inspect -f '{{.State.Health.Status}}' "$NAME")" in
            healthy) return 0 ;;
            unhealthy) fail "container became unhealthy" ;;
        esac
        sleep 2
    done
    fail "container did not become healthy"
}

echo "== Missing ALLOWED_HOSTS must stop the container"
if timeout 120 docker run --rm -e SECRET_KEY="$SECRET_KEY" \
        -v "$(mktemp -d):/data" "$IMAGE" > /dev/null 2>&1; then
    fail "container started without ALLOWED_HOSTS"
fi
echo "ok: refused to start"

echo "== Start"
docker run -d --name "$NAME" -p "${PORT}:80" -v "${DATA}:/data" \
    -e SECRET_KEY="$SECRET_KEY" -e ALLOWED_HOSTS=localhost "$IMAGE" > /dev/null
wait_healthy

expect 200 "$BASE/"
curl -s "$BASE/" | grep -q 'id="app"' || fail "/ is not the SPA"
expect 200 "$BASE/pins/1"  # SPA routes fall back to index.html
expect 200 "$BASE/api/v2/pins/"
expect 200 "$BASE/api/v2/schema/"
expect 200 "$BASE/api/v2/docs/"
expect 200 "$BASE/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-bundle.js"
expect 200 "$BASE/admin/login/"
expect 400 -H "Host: evil.example" "$BASE/api/v2/pins/"
docker logs "$NAME" 2>&1 | grep -q "Invalid HTTP_HOST header: 'evil.example'" \
    || fail "a rejected Host header is not in the container log"

echo "== Upload a pin"
TOKEN="$(docker exec "$NAME" python manage.py shell -c "
from users.models import User, create_token_if_necessary
user = User.objects.create_user('smoke', 'smoke@example.com', 'smoke-password-1')
print(create_token_if_necessary(user).key)
" | tail -n 1)"
AUTH="Authorization: Token ${TOKEN}"
IMAGE_ID="$(curl -sf -H "$AUTH" -F image=@docs/src/imgs/logo-dark.png \
    "$BASE/api/v2/images/" | python3 -c 'import json, sys; print(json.load(sys.stdin)["id"])')"
curl -sf -H "$AUTH" -H 'Content-Type: application/json' \
    -d "{\"image_by_id\": ${IMAGE_ID}, \"description\": \"smoke\", \"tags\": [\"smoke\"]}" \
    "$BASE/api/v2/pins/" > /dev/null || fail "creating the pin failed"
echo "ok: pin created"

echo "== Restart and check the pin and its file are still there"
docker restart "$NAME" > /dev/null
wait_healthy
THUMBNAIL="$(curl -sf "$BASE/api/v2/pins/" | python3 -c '
import json, sys
pins = json.load(sys.stdin)["results"]
assert len(pins) == 1, pins
print(pins[0]["image"]["thumbnail"]["image"])
')"
expect 200 "$(echo "$THUMBNAIL" | sed -E "s#^https?://[^/]+#${BASE}#")"

echo "All smoke checks passed."
