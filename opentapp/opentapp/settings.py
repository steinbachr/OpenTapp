"""
Django settings for opentapp project.

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
SECRET_KEY = 'r(4@-sn-6*_n8p!%krwws9-tfop!%*d6*0b-yp7s&8x#ivckh%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    ("barportal/templates/"),
)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'barportal',
    'south',
    'widget_tweaks',
    'rest_framework',
    'raven.contrib.django.raven_compat',
    'django_extensions',
    'captcha'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'opentapp.urls'

WSGI_APPLICATION = 'opentapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd8i9vq70pj5c52',
        'HOST': 'ec2-23-21-243-117.compute-1.amazonaws.com',
        'PORT': 5432,
        'USER': 'mrnqdsmygbbdbz',
        'PASSWORD': 'Cuyxlr2W_GYHWpOLPm5zwatnLl'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'barportal/static'
MEDIA_URL = '/media/'
MEDIA_ROOT = 'barportal/media'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'steinbach.rj@gmail.com'
EMAIL_HOST_PASSWORD = 'leonhall'
EMAIL_PORT = 587
EMAIL_USE_TLS = True