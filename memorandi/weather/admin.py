# memorandi.weather.admin
# Admin models registration
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Feb 11 20:00:01 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Admin models registration for weather app.
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from .models import *

##########################################################################
## Admin Registration
##########################################################################

admin.site.register(Weather)
