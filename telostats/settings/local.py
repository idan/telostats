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
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

LOGGING['handlers']['console']['level'] = 'DEBUG'

if DEBUG and not STATIC_S3:
    STATIC_URL = '/static/'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
