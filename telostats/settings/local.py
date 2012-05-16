from __future__ import absolute_import

import os
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

STATIC_S3 = 'STATIC_S3' in os.environ

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'telostats',
        'USER': 'telostats',
        'PASSWORD': 'telostats',
        'HOST': '',
        'PORT': '',
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
    },
}

LOGGING['handlers']['console']['level'] = 'DEBUG'

if DEBUG and not STATIC_S3:
    STATIC_URL = '/static/'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFileStorage'

# Celery
CELERY_RESULT_BACKEND = "redis"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 2
REDIS_CONNECT_RETRY = True

BROKER_BACKEND = 'redis'
BROKER_HOST = "localhost"  # Maps to redis host.
BROKER_PORT = 6379         # Maps to redis port.
BROKER_VHOST = "2"         # Maps to database number.
