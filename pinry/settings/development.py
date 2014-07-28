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
)

MIDDLEWARE_CLASSES += (
     'django.contrib.auth.middleware.AuthenticationMiddleware',
)

SECRET_KEY = 'fake-key'
