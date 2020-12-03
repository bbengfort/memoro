# memoro.settings.development
# Configuration for a development environment.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Nov 28 16:40:07 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: development.py [] benjamin@bengfort.com $

"""
Configuration for a development environment.
"""

##########################################################################
## Imports
##########################################################################

from .base import *  # noqa
from .base import PROJECT


##########################################################################
## Development Environment
##########################################################################

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

MEDIA_ROOT = PROJECT / 'tmp' / 'media'
STATIC_ROOT = PROJECT / 'tmp' / 'static'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Debugging email without SMTP
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = PROJECT / 'tmp' / 'outbox'
