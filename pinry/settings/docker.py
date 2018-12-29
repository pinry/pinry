import logging

from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
if 'SECRET_KEY' not in os.environ:
    logging.warning(
        "No SECRET_KEY given in environ, please have a check"
    )
SECRET_KEY = os.environ.get('SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: use your actual domain name in production!
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

USE_X_FORWARDED_HOST = True

try:
    from .local_settings import *
except ImportError:
    pass
