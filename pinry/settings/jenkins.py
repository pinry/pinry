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

SECRET_KEY = ''


INSTALLED_APPS += ('django_jenkins',)
PROJECT_APPS = (
    'pinry.vendor',
    'pinry.core',
    'pinry.pins',
    'pinry.api',
)


JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)
