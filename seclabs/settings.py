# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////////
from pathlib import Path
from datetime import datetime
#-----------------------------------------------------------------
#from celery.schedules import crontab 
 
#/////////////////////////////////////////////////////////////////
DEBUG = False
ALLOWED_HOSTS = ["*"]

#/////////////////////////////////////////////////////////////////
# Get project directories
ROOT_DIR    = str(Path(__file__).resolve().parent.parent)
PROJECT_DIR = str(Path(__file__).resolve().parent)

#/////////////////////////////////////////////////////////////////
# Local time zone for this installation.
TIME_ZONE = 'Europe/Dublin'

#/////////////////////////////////////////////////////////////////
# Django language settings
LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', 'English'),
)

LOCALE_PATHS = ( 
    PROJECT_DIR + '/locale/',
)

#///////////////////////////////////////////////////////////////// 
# Django encoding / timezone 
#/////////////////////////////////////////////////////////////////
USE_I18N = True
USE_L10N = True
USE_TZ = True

#/////////////////////////////////////////////////////////////////
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '--dummy--' # add-it

#/////////////////////////////////////////////////////////////////
# Encryption Settings
CRYPTO_SALT = "--dummy--"  # add-it
CRYPTO_NONCE = "--dummy--" # add-it

#/////////////////////////////////////////////////////////////////
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


#/////////////////////////////////////////////////////////////////
# Django email list
ADMINS = (
     ('seclabs team', '<team@seclabs.cc>'),
)
MANAGERS = ADMINS

#/////////////////////////////////////////////////////////////////
# Custom emails settings and url for email-templates
FROM = 'seclabs team <team@seclabs.com>'

#/////////////////////////////////////////////////////////////////
# Email Settings
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

#/////////////////////////////////////////////////////////////////
# Applications templates
TEMPLATES_DIR = PROJECT_DIR + '/templates'

#/////////////////////////////////////////////////////////////////
# Used as context_processor in embedded emails
SITE_URL = 'seclabs.com'
SITE_DOCS = 'seclabs.com/docs'
SITE_DATE = datetime.now().strftime("%Y")

#/////////////////////////////////////////////////////////////////
# Absolute path to the directory static files should be collected to.
STATIC_ROOT = PROJECT_DIR + '/style/'

#/////////////////////////////////////////////////////////////////
# URL prefix for static files.
STATIC_URL = '/style/'

#/////////////////////////////////////////////////////////////////
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = PROJECT_DIR + '/docs/'

#/////////////////////////////////////////////////////////////////
# URL that handles the media served from MEDIA_ROOT. 
MEDIA_URL = '/docs/'

#/////////////////////////////////////////////////////////////////
# Main Reports Folder
REPORTS = ROOT_DIR + '/reports'

#/////////////////////////////////////////////////////////////////
SECLABS_LOGO = STATIC_ROOT + 'dashboard/img/seclabs.png'

#/////////////////////////////////////////////////////////////////
# Login/Admin settings
LOGIN_REDIRECT_URL = '/dashboard/index/'
LOGIN_URL = '/login/'
FORCE_SCRIPT_NAME = ''

#///////////////////////////////////////////////////////////////// 
# Session Management
#SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SESSION_COOKIE_SECURE = True
#-----------------------------------------------------------------
#CSRF_COOKIE_SECURE = True
#CSRF_COOKIE_HTTPONLY = True
#CSRF_COOKIE_AGE = 31449600
#-----------------------------------------------------------------
#SECURE_SSL_REDIRECT = True

#/////////////////////////////////////////////////////////////////
WSGI_APPLICATION = 'seclabs.wsgi.application'

#///////////////////////////////////////////////////////////////// 
# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'seclabs.users',
    'seclabs.config',
    'seclabs.jira',
    'seclabs.asana',
    'seclabs.github',
    'seclabs.jumpcloud',
    'seclabs.dashboard',
]

#///////////////////////////////////////////////////////////////// 
# Middleware Setups
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#///////////////////////////////////////////////////////////////// 
# Root url config
ROOT_URLCONF = 'seclabs.urls'

#///////////////////////////////////////////////////////////////// 
# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'seclabs.processors.site_url',
                'seclabs.processors.site_date',
                'seclabs.processors.site_docs',
                'seclabs.processors.github_org',
            ],
        },
    },
]

#/////////////////////////////////////////////////////////////////
# Default primary key field type - Required since Django 3.2
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#///////////////////////////////////////////////////////////////// 
# Database - Backend configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ROOT_DIR + '/db.sqlite3',
    }
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': '',
#        'USER': '', 
#        'PASSWORD': '',
#        'HOST': '',
#        'PORT': '',
#    }
}

#/////////////////////////////////////////////////////////////////
# Results Settings
#-----------------------------------------------------------------
PAGES = 36

#/////////////////////////////////////////////////////////////////
# Filename/Path for Logger
LOG_FILE = ROOT_DIR + '/seclabs.log'
LOG_SIZE =  5242880 # (5MB)
LOG_PER_PAGE  = 50 # Paginator

#/////////////////////////////////////////////////////////////////
# Disabled logging
#----------------------------------------------------------------
# logging.disable(logging.INFO) 

#/////////////////////////////////////////////////////////////////
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s][%(pathname)s][%(lineno)d][%(levelname)s] [%(message)s]",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
            'maxBytes': LOG_SIZE,
            'backupCount': 5,
            'formatter': 'standard',
            },
        },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        'seclabs': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
    }
}
