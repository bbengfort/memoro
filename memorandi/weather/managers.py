# memorandi.weather.managers
# Manager classes for assisting with weather queries
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Feb 12 14:32:30 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: managers.py [] benjamin@bengfort.com $

"""
Manager classes for assisting with weather queries
"""

##########################################################################
## Imports
##########################################################################

from .wunder import Wunder
import utils.timez as timez
from django.db import models

##########################################################################
## Helper functions
##########################################################################

def hour_range(time=None):
    """
    Returns a tuple of the start of the hour and the end of an hour for a
    given time. If the timestamp is None, then uses the current time.
    """
    time = time or timez.now()
    head = time.replace(minute=0, second=0, microsecond=0)
    foot = time.replace(minute=59, second=59, microsecond=999999)
    return head, foot

##########################################################################
## Weather Managers
##########################################################################

class WeatherManager(models.Manager):

    def _request_weather(self, location):
        """
        Fetches the current weather from Weather Underground and stores it
        in the database. This method will fetch no matter what and since
        the API is rate limited, use with discretion!
        """
        if hasattr(location, 'to_query'):
            lookup = location.to_query()
        else:
            lookup = unicode(location)
        wunder = Wunder()
        response = wunder.fetch_weather(lookup, "conditions", "geolookup")
        if response.status_code == 200:
            data = response.json()
            conditions = data.get("current_observation", {})
            if conditions:
                obj = self.model.deserialize(conditions)
                obj.location = location
                obj.save(force_insert=True)
                return obj
            else:
                raise self.model.DoesNotExist("Bad data returned from WU API")
        else:
            raise self.model.DoesNotExist("Couldn't fetch data from WU API: %i: %s"
                                          % response.status_code, response.reason)

    def current_weather(self, location=None):
        """
        Returns the current weather for a particular location. This method
        will only query the API once every hour, so if there is weather
        with an observation within the current hour, it will return that,
        otherwise it will fetch the data from the API.

        Note: if the location is not specified, it returns the latest
        weather for the more recently added or modified location.

        Note: This method returns a single weather object.
        """
        query = self.get_queryset() # Base Query

        # Add filters based on time and location
        query = query.filter(observation__range=hour_range())
        if location:
            query = query.filter(location=location)

        # If query has nothing in it, get it via the API.
        if query.count() < 1:
            return self._request_weather(location)

        # Returnt he latest weather object.
        return query.latest()

if __name__ == '__main__':
    print hour_range()
