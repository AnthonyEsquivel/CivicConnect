# /***************************************************************************************
# *  REFERENCES
# *  Title: django-allauth | Installation
# *  Author: Raymond Penners
# *  Date: 2020
# *  Code version: 0.43.0
# *  URL: https://django-allauth.readthedocs.io/en/latest/installation.html
# *  Software License: MIT

# *
# *  Title: dj-database-url 
# *  Author: N/A
# *  Date: 3/1/2018
# *  Code version: 0.5.0
# *  URL: https://pypi.org/project/dj-database-url/
# *  Software License: PSF

# *  Title: Django Email/Contact Form Tutorial
# *  Author: Will Vincent
# *  Date:  Nov 10, 2020
# *  Code version: 3.0
# *  URL: https://learndjango.com/tutorials/django-email-contact-form#create-forms
# *  Software License: MIT
# ***************************************************************************************/

"""
Django settings for civic project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h_zpi@0!)#p!ecn#twc!ub*dvz=87vnsvmh4p^%rw*27zzddyc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'mainapp.apps.MainappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'civic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'civic.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

    #DATABASES = {
        #'default': {
            #'ENGINE': 'django.db.backends.sqlite3',
            #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        #}
    #}
DATABASES = { #ACTUAL DATABASE FOR PRODUCTION
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd94dieat1guf32',
        'USER': 'nhprcfctzchmmh',
        'PASSWORD': 'ab245f5eb7a3bf59c01b3dcf5877647f98066482521d6d2ca74a5cb030214c0b',
        'HOST': 'ec2-52-200-134-180.compute-1.amazonaws.com',
        'PORT': '5432',
        'TEST': {
            'NAME': 'd94dieat1guf32',
        }
    }
}
d = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(d)

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#Google authentication backend
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '565247049457-cijms5qgsqkgn8tga33seor1o0clmkr9.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'exQPMs9gEdTmlJ65-_cD63wl'


SITE_ID = 3
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

LOGOUT_URL='/'

LOGIN_URL = '/auth/login/google-oauth2/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# config/settings.py (new)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # new
DEFAULT_FROM_EMAIL = 'will@learndjango.com'
EMAIL_HOST = 'smtp.sendgrid.net' # new
EMAIL_HOST_USER = 'apikey' # new
EMAIL_HOST_PASSWORD = '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' # new
EMAIL_PORT = 587 # new
EMAIL_USE_TLS = True # new

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Activate Django-Heroku

try:
    # Configure Django App for Heroku
    import django_heroku

    django_heroku.settings(locals())
except ImportError:
    found = False
