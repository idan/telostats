import os
from unipath import FSPath as Path

PROJECT_DIR = Path(__file__).absolute().ancestor(2)

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'telostats'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Idan Gazit', 'idan@gazit.me'),
)
MANAGERS = ADMINS
INTERNAL_IPS = ('127.0.0.1',)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

TIME_ZONE = 'Etc/UTC'
USE_TZ = True
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = True

MEDIA_ROOT = PROJECT_DIR.child('media')
MEDIA_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/media'

STATIC_ROOT = PROJECT_DIR.child('static_root')
STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
STATICFILES_DIRS = (
    str(PROJECT_DIR.child('static')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)

ROOT_URLCONF = 'telostats.urls'
WSGI_APPLICATION = 'telostats.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',

    'gunicorn',
    'storages',
    'south',
    'djcelery',
    'tastypie',

    'telostats.stations',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Auth stuff
# LOGIN_REDIRECT_URL = '/profile'
# LOGIN_URL = '/login'
# LOGOUT_URL = '/logout'

# S3 Storage
# AWS_HEADERS = {
#     'Expires': 'Wed, 1 Jan 2020 00:00:00 GMT',
#     'Cache-Control': 'max-age=86400',
# }
# # AWS_PRELOAD_METADATA = True
# AWS_QUERYSTRING_AUTH = False
# from S3 import CallingFormat
# AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

# Tempo
TEMPODB_API_HOST = os.environ.get('TEMPODB_API_HOST')
TEMPODB_API_KEY = os.environ.get('TEMPODB_API_KEY')
TEMPODB_API_PORT = os.environ.get('TEMPODB_API_PORT')
TEMPODB_API_SECRET = os.environ.get('TEMPODB_API_SECRET')
TEMPODB_API_SECURE = os.environ.get('TEMPODB_API_SECURE')

# Celery
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "Etc/UTC"
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
import djcelery
djcelery.setup_loader()
