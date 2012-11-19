from __future__ import absolute_import

import dj_database_url
import urlparse

from os import environ
from .base import *

ENV = 'HEROKU'

# Store files on S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL'))
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'PASSWORD': redis_url.password,
            'DB': 1,
        },
    },
}

# Grab database info
DATABASES = {
    'default': dj_database_url.config()
}

# Setup sentry / raven
SENTRY_DSN = environ.get('SENTRY_DSN')
INSTALLED_APPS += (
    'raven.contrib.django',
)
