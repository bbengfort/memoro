# memorandi.settings.production
# Production environment specific settings
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Feb 11 09:42:27 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: production.py [] benjamin@bengfort.com $

"""
Production environment specific settings
"""

##########################################################################
## Imports
##########################################################################

from .base import *

##########################################################################
## Production Settings
##########################################################################

## Debugging Settings
DEBUG            = False
TEMPLATE_DEBUG   = False

## Hosts
ALLOWED_HOSTS    = []

## Content
STATIC_ROOT      = "/var/www/memorandi/static/"
MEDIA_ROOT       = "/var/www/memorandi/media/"
