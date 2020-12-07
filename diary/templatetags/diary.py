# diary.templatetags.diary
# Template tags and filters for the diary app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Mon Dec 07 16:12:15 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: diary.py [] benjamin@bengfort.com $

"""
Template tags and filters for the diary app
"""

##########################################################################
## Imports
##########################################################################

from django import template
from django.conf import settings

register = template.Library()


##########################################################################
## Template Tags
##########################################################################

@register.inclusion_tag("components/google_maps_js.html")
def google_maps_js():
    return {
        "api_key": settings.GOOGLE_JS_API_KEY,
    }

