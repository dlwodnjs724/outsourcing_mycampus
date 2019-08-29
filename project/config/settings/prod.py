from .common import *


DEBUG = False
ALLOWED_HOSTS = ['54.180.105.194']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'mycampus-cluster.cluster-ch0ryqkshdif.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'NAME': 'mycampus-cluster',
        'USER': 'admin',
        'PASSWORD': get_secret("mysql_PASSWORD"),
    }
}