# memoro.settings.production
# Configuration for production/deployment environment.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Nov 28 16:40:07 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: production.py [] benjamin@bengfort.com $

"""
Configuration for production/deployment environment.
"""

##########################################################################
## Imports
##########################################################################

from .base import *  # noqa
from .base import PROJECT


##########################################################################
## Production Environment
##########################################################################

# DEBUG should never be run in production, even with an environment variable
DEBUG = False

# Hosts
ALLOWED_HOSTS = [
    'memoro.us',
    'memoro.bengfort.com',
    'bengfort-memoro.herokuapp.com',
]

# Always use SSL
SECURE_SSL_REDIRECT = True

# Serve static files from inside project directory
STATIC_ROOT = PROJECT / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'