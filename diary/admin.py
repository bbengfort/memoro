# diary.admin
# Register models for admin management.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Dec 02 13:14:57 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Register models for admin management.
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from .models import Memo, Location, GeoEntity, Tabs

##########################################################################
## Register Admin Models
##########################################################################

admin.site.register(Memo)
admin.site.register(Location)
admin.site.register(GeoEntity)
admin.site.register(Tabs)