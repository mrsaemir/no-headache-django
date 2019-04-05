# settings file patched by no-headache-django

"""START OF PATCH"""

import os
import json

SECRET_KEY = os.environ.get('SECRET_KEY')
# Debug Info
# never use DEBUG=True in production.
DEBUG_ENVVAR = os.environ.get('DEBUG', '')
# because an envvar is just a string and each string is considered True
# in python we have to determine if the boolean is True or False
DEBUG = False
if DEBUG_ENVVAR.lower() == "true":
    DEBUG = True

ALLOWED_HOSTS = json.loads(os.environ.get('ALLOWED_HOSTS'))

# DB configurations
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT'),
        'OPTIONS': {
          'autocommit': True,
        },
    }
}

STATIC_URL = os.environ.get('STATIC_URL')
MEDIA_URL = os.environ.get('MEDIA_URL')

STATIC_ROOT = "/static/"
MEDIA_ROOT = '/media/'

"""END OF PATCH"""
