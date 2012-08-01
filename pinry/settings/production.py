from pinry.settings import *

import os


DEBUG = False
TEMPLATE_DEBUG = DEBUG

# TODO: I recommend using psycopg2 w/ postgres but sqlite3 is good enough.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'production.db'),
    }
}

# TODO: Be sure to set this.
SECRET_KEY = ''
