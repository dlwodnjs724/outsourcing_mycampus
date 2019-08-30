from .common import *


DEBUG = False
ALLOWED_HOSTS = ['54.180.98.242', 'mycampus.site', 'www.mycampus.site']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'mycampus',
        'USER': 'mycampus',
        'PASSWORD': 'mycampus123',
    }
}