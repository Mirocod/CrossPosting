from os import path
from pathlib import Path

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-aaaa'

SALT = 'aaaaaaaa'
ALLOWED_HOSTS = ['localhost']

CSRF_TRUSTED_ORIGINS = ['http://zakonvremeni.ru:8989',]

LOG_DIR = path.join(Path(__file__).resolve().parent.parent.parent, 'logs/')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s]- %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR + 'application.log',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
