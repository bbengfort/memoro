# memorandi.settings.base
# Default Django settings for entire Memorandi project
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Feb 11 09:34:40 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: base.py [] benjamin@bengfort.com $

"""
Django settings for memorandi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

##########################################################################
## Imports
##########################################################################

import os
from django.core.urlresolvers import reverse_lazy

##########################################################################
## Helper function for environmental settings
##########################################################################

def environ_setting(name, default=None):
    """
    Fetch setting from the environment- if not found, then this setting is
    ImproperlyConfigured.
    """
    if name not in os.environ and default is None:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "The {0} ENVVAR is not set.".format(name)
        )

    return os.environ.get(name, default)

##########################################################################
## Build Paths inside of project with os.path.join
##########################################################################

BASE_DIR    = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.normpath(os.path.join(BASE_DIR, os.pardir))

##########################################################################
## Secret settings - do not store!
##########################################################################

SECRET_KEY = environ_setting("SECRET_KEY")

##########################################################################
## Database Settings
##########################################################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ_setting('DB_NAME', 'memorandi'),
        'USER': environ_setting('DB_USER', 'django'),
        'PASSWORD': environ_setting('DB_PASS'),
        'HOST': environ_setting('DB_HOST', 'localhost'),
        'PORT': environ_setting('DB_PORT', '5432'),
    },
}

##########################################################################
## Runtime settings
##########################################################################

## Debugging Settings
DEBUG            = False
TEMPLATE_DEBUG   = False

## Hosts
ALLOWED_HOSTS    = []

## WSGI Configuration
ROOT_URLCONF     = 'memorandi.urls'
WSGI_APPLICATION = 'memorandi.wsgi.application'

## Application Definition
INSTALLED_APPS   = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'taggit',
    'location',
    'weather',
    'narrate',
    'authors',
    'api',
)

## Request Handling
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'authors.middleware.AuthorMiddleware',
)

## Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'America/New_York'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True

## Login URLs
LOGIN_REDIRECT_URL = reverse_lazy('app-root')   # Named pattern for the application root
LOGIN_URL          = reverse_lazy('LoginView')  # Named pattern for the login class
LOGOUT_URL         = reverse_lazy('LogoutView') # Named pattern for the logout class
# Note: For some reason, even though we're in Django 1.6 simply using the
# name of the view did not work as expected. Reverse lazy does work though.

##########################################################################
## Content (Static, Media, Templates)
##########################################################################

## Static Files
STATIC_URL          =  '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS    = (
    os.path.join(PROJECT_DIR, 'static'),
)

## Template Files.
TEMPLATE_DIRS       = (
    os.path.join(PROJECT_DIR, 'templates'),
)

## Uploaded Media
MEDIA_URL           = "/media/"

## User Stuf
AUTH_PROFILE_MODULE = "authors.Profile"

## Suit Admin Config
SUIT_CONFIG         = {
    "ADMIN_NAME": "Memorandi Admin",
    "MENU_ICONS": {
        "auth": "icon-user",
        "location": "icon-map-marker",
        "weather": "icon-leaf",
        "taggit": "icon-tags",
        "narrate": "icon-book",
    }
}

## Template Context Processors
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "authors.context_processors.author",
)

##########################################################################
## Logging and Error Reporting
##########################################################################

ADMINS          = (
    ('Benjamin Bengfort', 'benjamin@bengfort.com'),
)

SERVER_EMAIL    = 'Dakota <server@bengfort.com>'
EMAIL_USE_TLS   = True
EMAIL_HOST      = 'smtp.gmail.com'
EMAIL_HOST_USER = 'server@bengfort.com'
EMAIL_HOST_PASSWORD = environ_setting("EMAIL_HOST_PASSWORD")
EMAIL_PORT      = 587

##########################################################################
## REST Framework
##########################################################################

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
    'rest_framework.serializers.HyperlinkedModelSerializer',

    # Filtering support
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'PAGINATE_BY': 10,
}

##########################################################################
## External Services
##########################################################################

WEATHER_UNDERGROUND = {
    "API_KEY": environ_setting("WUNDER_API_KEY", ""), # Default is empty key
}

GEOIP2_PATH    = environ_setting("GEOIP2_PATH", "")                 # Default is current working directory
GEOIP2_CITY    = os.path.join(GEOIP2_PATH, "GeoLite2-City.mmdb")    # City MMDB database
GEOIP2_COUNTRY = os.path.join(GEOIP2_PATH, "GeoLite2-Country.mmdb") # Country MMDB database
