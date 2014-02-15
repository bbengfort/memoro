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

import os
import urllib
import requests
import urlparse
import w3lib.url

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

##########################################################################
## Module constants
##########################################################################

# Known Data Features exposed by Weather Underground API
DATA_FEATURES = (
    'alerts', 'almanac', 'astronomy', 'conditions', 'currenthurricane',
    'forecast', 'forecast10day', 'geolookup', 'history', 'hourly',
    'hourly10day', 'planner', 'rawtide', 'satellite', 'tide', 'webcams',
    'yesterday'
)

##########################################################################
## Helper functions
##########################################################################

def urljoin(*parts):
    """
    Helper function for constructing endpoints
    """
    url = urlparse.urljoin(*parts)
    if not url.endswith('/'):
        url += '/'
    return w3lib.url.safe_download_url(url)

##########################################################################
## Wunder Object
##########################################################################

class Wunder(object):
    """
    Manages the retrieval of weather data from Weather Underground.

    The Weather Underground API operates by constructing a base URL
    request along with an API key that you must apply for on their site.
    You can then request any number of data features, chained together in
    the endpoint. You terminate the data features with a 'q' path and then
    provide the parameters of the query, typically geography. The datatype
    is specified by the extension at the end of the request.

        http://api.wunderground.com/api/apikey/features/settings/q/query.format

    For example, the endpoint:

        http://api.wunderground.com/api/apikey/geolookup/conditions/q/IA/Cedar_Rapids.json

    Looks up the geography and conditions of Cedar Rapids, IA and expects
    a JSON response in return. The API Key must be registered.
    """

    BASE_URL = "http://api.wunderground.com/api/"

    def __init__(self, apikey=None):
        self.apikey = apikey

    @property
    def apikey(self):
        return self._apikey

    @apikey.setter
    def apikey(self, key):
        """
        Fetch key from settings if not provided at init.
        """
        if key is None:
            key = settings.WEATHER_UNDERGROUND.get('API_KEY', None)
        if not key:
            raise ImproperlyConfigured('No Weather Underground API Key set.')
        self._apikey = key

    @property
    def urlbase(self):
        """
        Returns the base endpoint with the API KEY included. Trailing
        slash required to ensure other urljoins work as expected.
        """
        return urljoin(self.BASE_URL, self.apikey)

    def get_features_endpoint(self, *features):
        """
        Data features provided by the Weather Underground API.
        """

        # Validation
        for feature in features:
            if feature not in DATA_FEATURES:
                raise NotImplementedError("Unknown feature: '%s'" % feature)

        # Construct endpoint
        uri = os.path.join(os.path.join(*features), 'q')
        return urljoin(self.urlbase, uri)

    def get_query_endpoint(self, query, *features, **kwargs):
        """
        Constructs a complete endpoint from the query, features, and
        and format of the request. Note that this method does not support
        additional (optional) settings at this point. The query itself
        can be as follows:


            CA/San_Francisco    US state/city
            60290               US zipcode
            Australia/Sydney    country/city
            37.8,-122.4         latitude,longitude
            KJFK                airport code
            pws:KCASANFR70      PWS id
            autoip              AutoIP address location

        Note: This method also currently does not perform any validation.
        Note: This method doesn't take any parameters to constuct on endpoint

        Note: This should be the entrypoint for all endpoint constructors
        """
        frmt  = kwargs.pop('format', 'json')
        url   = self.get_features_endpoint(*features)
        query = urllib.quote(".".join((query, frmt)))
        return w3lib.url.safe_download_url(urlparse.urljoin(url, query))

    def fetch_weather(self, query, *features, **kwargs):
        """
        Actually makes the request to Weather Underground and return the
        HTTP Response from the API Service. Default features is conditions.
        """
        if not features: features = ('conditions',)
        endpoint = self.get_query_endpoint(query, *features, **kwargs)
        return requests.get(endpoint)

if __name__ == '__main__':
    import json
    wunder = Wunder()
    print json.dumps(wunder.fetch_weather("DC/Washington").json)
