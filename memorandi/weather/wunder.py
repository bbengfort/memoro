# memorandi.weather.wunder
# Wrapper to fetch Weather Underground data
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Feb 12 11:05:04 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: wunder.py [] benjamin@bengfort.com $

"""
Wrapper to fetch Weather Underground data
"""

##########################################################################
## Imports
##########################################################################

import requests

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

##########################################################################
## Wunder Object
##########################################################################

class Wunder(object):
    """
    Manages the retrieval of weather data from Weather Underground
    """

    def __init__(self, apikey=None):
        self.apikey = apikey

    @property
    def apikey(self):
        return self._apikey

    @apikey.setter
    def apikey(self, key):
        if key is None:
            key = settings.WEATHER_UNDERGROUND.get('API_KEY', None)
        if not key:
            raise ImproperlyConfigured('No Weather Underground API Key set.')
        self._apikey = key
