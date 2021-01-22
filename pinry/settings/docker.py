from distutils import util
import logging

from .base import *

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
SECRET_KEY = os.environ.get('SECRET_KEY')
STATIC_ROOT = '/data/static'
USE_X_FORWARDED_HOST = True

ALLOW_NEW_REGISTRATIONS = bool(util.strtobool(
    os.environ.get('ALLOW_NEW_REGISTRATIONS', 'True')
))
DEBUG = bool(util.strtobool(
    os.environ.get('DEBUG', 'False')
))
IMAGE_AUTO_DELETE = bool(util.strtobool(
    os.environ.get('IMAGE_AUTO_DELETE', 'True')
))
PUBLIC = bool(util.strtobool(
    os.environ.get('PUBLIC_PINS', 'True')
))

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'PORT': 5432,
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
    }
}

IMAGE_SIZES = {
    'thumbnail': {'size': [240, 0]},
    'standard': {'size': [600, 0]},
    'square': {'crop': True, 'size': [125, 125]},
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]
