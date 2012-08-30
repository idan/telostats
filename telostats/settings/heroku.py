from __future__ import absolute_import
import os
import urlparse
from .base import *

# Store files on S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Pull the various config info from Heroku.

# Make sure urlparse understands custom config schemes.
urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('redis')

# Grab database info
#db_url = urlparse.urlparse(os.environ['DATABASE_URL'])
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

# Now do redis
redis_url = urlparse.urlparse(os.environ['REDISTOGO_URL'])

# Use redis for cache
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{0}:{1}'.format(redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': redis_url.password,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
    },
}

# Also use redis for celery
CELERY_RESULT_BACKEND = "redis"
REDIS_HOST = CELERY_REDIS_HOST = redis_url.hostname
REDIS_PORT = CELERY_REDIS_PORT = redis_url.port
REDIS_PASSWORD = CELERY_REDIS_PASSWORD = redis_url.password
REDIS_DB = CELERY_REDIS_DB = 0
REDIS_CONNECT_RETRY = True
BROKER_BACKEND = "redis"
BROKER_TRANSPORT = "redis"
BROKER_HOST = redis_url.hostname
BROKER_PORT = int(redis_url.port)
BROKER_PASSWORD = redis_url.password

# Lock down some security stuff.
# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_HTTPONLY = True
# SECURE_SSL_REDIRECT = True
# SECURE_FRAME_DENY = True
# SECURE_HSTS_SECONDS = 6000
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if 'SENTRY_DSN' in os.environ:
    try:
        import raven
        # Add raven to the list of installed apps
        INSTALLED_APPS += ('raven.contrib.django',)
    except Exception, e:
        print "Unable to import raven: ", e
        traceback.print_exc()
