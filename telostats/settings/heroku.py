from __future__ import absolute_import

import dj_database_url

from os import environ
from .base import *

# Store files on S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Grab database info
DATABASES = {
    'default': dj_database_url.config()
}

# Setup sentry / raven
SENTRY_DSN = environ.get('SENTRY_DSN')
INSTALLED_APPS += (
    'raven.contrib.django',
)
