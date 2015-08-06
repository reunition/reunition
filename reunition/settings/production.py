import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

# IMPORTANT!:
# You must keep this secret, you can store it in an
# environment variable and set it with:
# export SECRET_KEY="phil-dunphy98!-bananas12"
# https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/#secret-key
SECRET_KEY = os.environ['SECRET_KEY']

## WSGI SETTINGS
# https://docs.djangoproject.com/en/1.8/ref/settings/#wsgi-application
WSGI_APPLICATION = 'reunition.wsgi.application'

## NOTIFICATIONS
# A tuple that lists people who get code error notifications.
# https://docs.djangoproject.com/en/1.8/ref/settings/#admins
ADMINS = (
#    ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

## DJANGO-COMPRESSOR SETTINGS
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)
STATICFILES_FINDERS = STATICFILES_FINDERS + (
    'compressor.finders.CompressorFinder',
)
COMPRESS_OFFLINE = True

try:
    from local_settings import *
except ImportError:
    pass
