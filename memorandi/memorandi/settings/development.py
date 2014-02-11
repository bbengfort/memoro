# memorandi.settings.development
# Development environment specific settings
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Feb 11 09:41:29 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: development.py [] benjamin@bengfort.com $

"""
Development environment specific settings
"""

##########################################################################
## Imports
##########################################################################

from .base import *

##########################################################################
## Development Settings
##########################################################################

## Debugging Settings
DEBUG            = True
TEMPLATE_DEBUG   = True

## Hosts
ALLOWED_HOSTS    = ('127.0.0.1', 'localhost')

## Secret Key doesn't matter in Dev
SECRET_KEY = 'ag05z*%5)$+wccf@anpqe+u@7-^b#%=&9gezq64*ox2d#7v&&r'
