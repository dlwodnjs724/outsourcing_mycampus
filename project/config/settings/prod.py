from .common import *


DEBUG = False
ALLOWED_HOSTS = ['54.180.105.194']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'mycampus',
        'USER': 'mycampus',
        'PASSWORD': 'mycampus123',
    }
}