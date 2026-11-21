"""Docker HEALTHCHECK: nginx serves the SPA and gunicorn answers the API."""
import os
import sys
import urllib.error
import urllib.request


def host_header():
    # Django answers 400 to a Host it doesn't allow, so use an allowed one.
    for host in os.environ.get('ALLOWED_HOSTS', '').split(','):
        host = host.strip().lstrip('.')
        if host and host != '*':
            return host
    return 'localhost'


def status(path):
    request = urllib.request.Request(
        'http://127.0.0.1' + path, headers={'Host': host_header()},
    )
    try:
        with urllib.request.urlopen(request, timeout=4) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code


# With PUBLIC=false the API answers 403 to anonymous requests; that still
# means it is up. Only a 5xx (or no answer) is unhealthy.
try:
    healthy = status('/') == 200 and status('/api/v2/') < 500
except OSError:
    healthy = False
sys.exit(0 if healthy else 1)
