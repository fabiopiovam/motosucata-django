"""
Django settings for motosucata project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Generate your code here http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
LOCAL = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

ALLOWED_HOSTS = ["*"]

DEFAULT_FROM_EMAIL = 'fabio@laborautonomo.org'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


try:
    from settings_production import *
except ImportError:
    pass

try:
    from settings_local import *
except ImportError:
    pass


ROOT_URLCONF = 'motosucata.urls'

WSGI_APPLICATION = 'motosucata.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-br' #'en-us'

TIME_ZONE = 'America/Sao_Paulo' #'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#TEMPLATE_DIRS = ('/home/templates/mike', '/home/templates/john')
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates')
)

REDACTOR_OPTIONS = {'lang': 'pt_br', 'focus':False}
REDACTOR_UPLOAD = 'static/'

THUMBNAIL_ALIASES = {
    '': {
        'medium': {'size': (425, 425), 'crop': 'smart'},
        'small': {'size': (140, 140), 'crop': 'smart'},
    },
}

# Flexselect settings.
FLEXSELECT = {
    'include_jquery': True,
}


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'easy_thumbnails',
    'redactor',
    'flexselect',
    
    'products',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)