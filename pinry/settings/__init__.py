import os

from django.contrib.messages import constants as messages


SITE_ROOT = os.path.join(os.path.realpath(os.path.dirname(__file__)), '../../')


# Changes the naming on the front-end of the website.
SITE_NAME = 'Pinry'

# Set to False to disable people from creating new accounts.
ALLOW_NEW_REGISTRATIONS = True

# Set to False to force users to login before seeing any pins. 
PUBLIC = True


TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True


MEDIA_URL = '/media/'
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
TEMPLATE_DIRS = [os.path.join(SITE_ROOT, 'pinry/templates')]
STATICFILES_DIRS = [os.path.join(SITE_ROOT, 'pinry/static')]


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pinry.users.middleware.Public',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'pinry.core.context_processors.template_settings',
)
AUTHENTICATION_BACKENDS = (
    'pinry.users.auth.backends.CombinedAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)


ROOT_URLCONF = 'pinry.urls'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
INTERNAL_IPS = ['127.0.0.1']
MESSAGE_TAGS = {
    messages.WARNING: 'alert',
    messages.ERROR: 'alert alert-error',
    messages.SUCCESS: 'alert alert-success',
    messages.INFO: 'alert alert-info',
}
API_LIMIT_PER_PAGE = 50


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'taggit',
    'compressor',
    'django_images',
    'pinry.core',
    'pinry.users',
)

IMAGE_PATH = 'pinry.core.utils.upload_path'
IMAGE_SIZES = {
    'thumbnail': {'size': [240, 0]},
    'standard': {'size': [600, 0]},
    'square': {'crop': True, 'size': [125, 125]},
}
