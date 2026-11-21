from .base import *


DEBUG = True

# Development defaults; environment variables still win.
SECRET_KEY = SECRET_KEY or 'REPLACE-ME'

ALLOWED_HOSTS = ALLOWED_HOSTS or ['*']

INSTALLED_APPS += [
    'django_extensions',
]
