from django.core.exceptions import ImproperlyConfigured

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Everything lives in the /data volume.
STATIC_ROOT = '/data/static'

MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')

DATABASES = {
    'default': dj_database_url.parse(
        env_str('DATABASE_URL', 'sqlite:////data/production.db'),
    ),
}

USE_X_FORWARDED_HOST = True

# Set HTTPS=true when Pinry is served over HTTPS by a reverse proxy that sets
# X-Forwarded-Proto. Cookies are then only sent over HTTPS.
if env_flag('HTTPS'):
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HSTS makes browsers refuse plain HTTP for this many seconds. Only set it
# once HTTPS works, since browsers remember it.
SECURE_HSTS_SECONDS = env_int('HSTS_SECONDS', 0)

# Django only prints errors to the console when DEBUG is on, so by default
# a rejected Host header (400 Bad Request) left no trace in
# `docker compose logs`. Send warnings and errors to stderr, which gunicorn
# passes on to the container log.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'one_line': {
            '()': 'pinry.log.OneLineFormatter',
            'format': '%(levelname)s %(name)s: %(message)s',
        },
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'security': {
            'class': 'logging.StreamHandler',
            'formatter': 'one_line',
        },
    },
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'WARNING'},
        # e.g. "Invalid HTTP_HOST header: 'localhost'. You may need to add
        # 'localhost' to ALLOWED_HOSTS."
        'django.security': {
            'handlers': ['security'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]

if not SECRET_KEY:
    raise ImproperlyConfigured(
        "SECRET_KEY is not set. Set it in the environment, for example "
        "with the output of docker/scripts/gen_key.sh."
    )

if not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "ALLOWED_HOSTS is not set. Set it in the environment to the host "
        "names and addresses Pinry is reached at, comma separated, e.g. "
        "\"pins.example.com,192.168.1.10\"."
    )
