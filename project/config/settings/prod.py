from .common import *


DEBUG = False
ALLOWED_HOSTS = ['15.164.118.64', 'mycampus.site']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'mycampus',
        'USER': 'mycampus',
        'PASSWORD': 'mycampus123',
    }
}