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
from reading.models import ArticleCounts
from diary.models import Memo, Location, GeoEntity, Tabs


##########################################################################
## Admin Forms
##########################################################################

class ArticleCountsInline(admin.StackedInline):

    model = ArticleCounts

class TabsInline(admin.StackedInline):

    model = Tabs


class MemoAdmin(admin.ModelAdmin):

    inlines = [
        TabsInline, ArticleCountsInline
    ]


##########################################################################
## Register Admin Models
##########################################################################

admin.site.register(Memo, MemoAdmin)
admin.site.register(Location)
admin.site.register(GeoEntity)