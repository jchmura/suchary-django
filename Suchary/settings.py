"""
Django settings for Suchary project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import logging

from Suchary.logging.filters import RangeFilter


try:
    from .local_settings import *
except ImportError:
    pass

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# in local settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates/'),
    os.path.join(BASE_DIR, 'templates/admin/'),
    os.path.join(BASE_DIR, 'templates/base/')
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ALLOWED_HOSTS = [
    'suchary.jakubchmura.pl', '95.85.63.30',
    'dev.jakubchmura.pl', '178.62.202.193'
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
    'django_filters',
    'reversion',

    'obcy',
    'api',
    'accounts'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'reversion.middleware.RevisionMiddleware',
)

ROOT_URLCONF = 'Suchary.urls'

WSGI_APPLICATION = 'Suchary.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# in local_settings

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Media file
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'),)
STATIC_URL = '/static/'

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',
    'PAGINATE_BY': 15,
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django-cache',
    }
}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 2
CACHE_MIDDLEWARE_KEY_PREFIX = 'default'

LOG_DIR = os.path.join(BASE_DIR, 'logs/')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'filters': {
        'info': {
            '()': RangeFilter,
            'min': logging.INFO,
            'max': logging.INFO
        },
        'warning': {
            '()': RangeFilter,
            'min': logging.WARNING
        }
    },
    'handlers': {
        'all': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + '/all.log',
            'maxBytes': 1024 * 1024,
            'formatter': 'simple'
        },
        'info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + '/info.log',
            'maxBytes': 1024 * 1024,
            'formatter': 'simple',
            'filters': ['info']
        },
        'warning': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + '/warning.log',
            'maxBytes': 1024 * 1024,
            'formatter': 'simple',
            'filters': ['warning']
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['all', 'info', 'warning'],
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = LOG_DIR + '/mail'

try:
    from .dev_settings import *
except ImportError:
    pass
