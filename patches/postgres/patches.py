# settings file patched by no-headache-django

"""START OF PATCH"""

from json import loads
from os import environ

SECRET_KEY = environ.get('SECRET_KEY')
# Debug Info
# never use DEBUG=True in production.
DEBUG_ENVVAR = environ.get('DEBUG', '')
# because an envvar is just a string and each string is considered True
# in python we have to determine if the boolean is True or False
DEBUG = False
if DEBUG_ENVVAR.lower() == "true":
    DEBUG = True

ALLOWED_HOSTS = loads(environ.get('ALLOWED_HOSTS'))

# DB configurations
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ.get('DB_NAME'),
        'USER': environ.get('DB_USER'),
        'PASSWORD': environ.get('DB_PASSWORD'),
        'HOST': environ.get('DB_HOST'),
        'PORT': environ.get('DB_PORT'),
    }
}

STATIC_URL = environ.get('STATIC_URL')
MEDIA_URL = environ.get('MEDIA_URL')

STATIC_ROOT = "/static/"
MEDIA_ROOT = '/media/'

"""END OF PATCH"""
