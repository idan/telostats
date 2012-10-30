import os
from unipath import FSPath as Path

PROJECT_DIR = Path(__file__).absolute().ancestor(2)

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_CUSTOM_DOMAIN = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False
TILESERVER_URL = os.environ.get('TILESERVER_URL')

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
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
# the following line is a total lie
MEDIA_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '/media'

STATIC_ROOT = PROJECT_DIR.child('static_root')
STATICFILES_ROOT = PROJECT_DIR.child('static')
STATIC_URL = '//' + AWS_STORAGE_BUCKET_NAME
STATICFILES_DIRS = [
    (subdir, str(STATICFILES_ROOT.child(subdir))) for subdir in
    ['css', 'fonts', 'img', 'js']]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
STATICFILES_STORAGE = 'telostats.utils.storages.ProtocolRelativeS3BotoStorage'

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

EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER')
EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')
EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT')
EMAIL_USE_TLS = True
SERVER_EMAIL = 'admin@telostats.com'
DEFAULT_FROM_EMAIL = SERVER_EMAIL
