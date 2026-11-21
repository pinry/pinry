import os

import dj_database_url
from django.contrib.messages import constants as messages

from .env import env_flag, env_int, env_json, env_list, env_str


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# All site settings come from environment variables; see .env.example.

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_str('SECRET_KEY', '')

# Host names (and LAN addresses) Pinry answers to, e.g.
# "pins.example.com,192.168.1.10".
ALLOWED_HOSTS = env_list('ALLOWED_HOSTS')

# Origins with a scheme, e.g. "https://pins.example.com". Only needed when
# a proxy changes the host or scheme the browser sees.
CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS')

# e.g. "postgres://user:password@db:5432/pinry"; SQLite by default.
DATABASES = {
    'default': dj_database_url.parse(env_str(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
    )),
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'taggit',
    'django_images',
    'core',
    'users',
    'pinry_plugins.apps.PinryPluginsConfig',
]

ROOT_URLCONF = 'pinry.urls'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pinry.middleware.ForceCSRFCookieMiddleware',
    'users.middleware.Public',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'pinry/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.template_settings',
            ],
        },
    },
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'pinry/static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')

WSGI_APPLICATION = 'pinry.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

# Set to False to disable people from creating new accounts.
ALLOW_NEW_REGISTRATIONS = env_flag('ALLOW_NEW_REGISTRATIONS', True)

# Set to False to force users to login before seeing any pins.
PUBLIC = env_flag('PUBLIC', True)

AUTHENTICATION_BACKENDS = [
    'users.auth.backends.CombinedAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'

MESSAGE_TAGS = {
    messages.WARNING: 'alert alert-warning',
    messages.ERROR: 'alert alert-danger',
    messages.SUCCESS: 'alert alert-success',
    messages.INFO: 'alert alert-info',
}

API_LIMIT_PER_PAGE = 50

IMAGE_PATH = 'core.utils.upload_path'

# Thumbnail sizes, as JSON in the IMAGE_SIZES environment variable.
IMAGE_SIZES = env_json('IMAGE_SIZES', {
    'thumbnail': {'size': [240, 0]},
    'standard': {'size': [600, 0]},
    'square': {'crop': True, 'size': [125, 125]},
})

# IS_TEST is a variable to mark if the test is running
IS_TEST = False

# Delete image files once their last pin is removed.
IMAGE_AUTO_DELETE = env_flag('IMAGE_AUTO_DELETE', True)

# Set to True to let users pin images from loopback, private (LAN),
# link-local and other non-public addresses. Only do this if you trust
# every account holder, since it lets them reach internal services.
ALLOW_PRIVATE_URL_FETCH = env_flag('ALLOW_PRIVATE_URL_FETCH', False)

# Largest image, in bytes, that Pinry will download when pinning by URL.
MAX_FETCH_BYTES = env_int('MAX_FETCH_BYTES', 50 * 1024 * 1024)

# Set to True to accept HTTP Basic auth (username and password on every
# request) on the API. Off by default; API clients should use a token.
ALLOW_BASIC_AUTH = env_flag('ALLOW_BASIC_AUTH', False)

# Plugin classes to load, comma separated; see docs/src/plugin-system.md.
ENABLED_PLUGINS = env_list('ENABLED_PLUGINS')

# Rest Framework

DRF_URL_FIELD_NAME = "resource_link"

_login_rate = env_str('LOGIN_THROTTLE_RATE', '20/hour')

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'URL_FIELD_NAME': DRF_URL_FIELD_NAME,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': API_LIMIT_PER_PAGE,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'users.auth.throttling.OptionalBasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    # Failed password checks per client address, for the login view and
    # Basic auth. LOGIN_THROTTLE_RATE=off disables it.
    'DEFAULT_THROTTLE_RATES': {
        'login': _login_rate if _login_rate.lower() != 'off' else None,
    },
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Pinry API',
    'SERVE_INCLUDE_SCHEMA': False,
    # Serve Swagger UI from /static, not a CDN, so the docs work offline.
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}
