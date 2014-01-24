from pinry.settings import *

import os


DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'development.db'),
    }
}

INSTALLED_APPS += (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
)

MIDDLEWARE_CLASSES += (
     'django.middleware.common.CommonMiddleware',
     'django.contrib.messages.middleware.MessageMiddleware',
     'django.contrib.sessions.middleware.SessionMiddleware',
     'django.contrib.auth.middleware.AuthenticationMiddleware',
)

SECRET_KEY = 'fake-key'
