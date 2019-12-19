import logging

from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
if 'SECRET_KEY' not in os.environ:
    logging.warning(
        "No SECRET_KEY given in environ, please have a check."
        "If you have a local_settings file, please ignore this warning."
    )
SECRET_KEY = os.environ.get('SECRET_KEY', "PLEASE_REPLACE_ME")

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

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]

# should not ignore import error in production, local_settings is required
from .local_settings import *
