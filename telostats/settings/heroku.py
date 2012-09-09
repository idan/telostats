from __future__ import absolute_import
import os
import urlparse
from .base import *

# Store files on S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Pull the various config info from Heroku.

# Make sure urlparse understands custom config schemes.
urlparse.uses_netloc.append('postgres')

# Grab database info
db_url = urlparse.urlparse(os.environ['HEROKU_POSTGRESQL_NAVY_URL'])
DATABASES = {
    'default': {
        'ENGINE':  'django.db.backends.postgresql_psycopg2',
        'NAME':     db_url.path[1:],
        'USER':     db_url.username,
        'PASSWORD': db_url.password,
        'HOST':     db_url.hostname,
        'PORT':     db_url.port,
    }
}

if 'SENTRY_DSN' in os.environ:
    try:
        import raven
        # Add raven to the list of installed apps
        INSTALLED_APPS += ('raven.contrib.django',)
    except Exception, e:
        print "Unable to import raven: ", e
        traceback.print_exc()
