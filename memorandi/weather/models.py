# memorandi.weather.models
# Models for the Weather meta information
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Feb 11 18:06:42 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Models for the Weather meta information
"""

##########################################################################
## Imports
##########################################################################

from utils import nullable
from django.db import models
from .managers import WeatherManager
from model_utils.models import TimeStampedModel
from utils.timez import strptimez, RFC822_DATETIME

##########################################################################
## Models
##########################################################################

class Weather(TimeStampedModel):
    """
    A historical picture of weather stored in the database and referenced
    to by the memos. This weather model is currently fetched from the
    Weather Underground API.
    """

    station_id  = models.CharField( max_length=255, **nullable )   # The ID of the weather station
    observation = models.DateTimeField( **nullable )               # The time of the observation
    weather     = models.CharField( max_length=255, **nullable )   # Description of the weather
    temp        = models.CharField( max_length=255, **nullable )   # Textual description of temperature
    temp_cels   = models.FloatField( **nullable )  # Temperature in degrees Celsius
    temp_fahr   = models.FloatField( **nullable )  # Temperature in degrees Fahrenheit
    wind        = models.CharField( max_length=255, **nullable )   # Description of the wind
    wind_dir    = models.CharField( max_length=32, **nullable )   # Compass direction of the wind
    wind_degree = models.IntegerField( **nullable )  # Degree of wind direction
    wind_mph    = models.FloatField( **nullable )    # Speed of wind in MPH
    wind_gust_mph = models.FloatField( **nullable )  # Gust speed of wind in MPH
    pressure    = models.IntegerField( **nullable )  # Pressure in millibars
    dewpoint    = models.CharField( max_length=255, **nullable )   # Textual Description of Dewpoint
    precipitation = models.CharField( max_length=255, **nullable ) # Textual Description of Precipitation
    icon        = models.CharField( max_length=255, **nullable )   # Icon of weather
    location    = models.ForeignKey( "location.Location", related_name="weather")

    # Weather manager
    objects     = WeatherManager()

    class Meta:
        db_table        = "weather"
        verbose_name    = "weather"
        unique_together = ("station_id", "observation")
        ordering        = ["-observation",]
        get_latest_by   = "observation"
        verbose_name_plural = "weather"

    def __unicode__(self):
        return "%s on %s" % (self.weather, self.observation)

    @classmethod
    def deserialize(klass, data):
        """
        Constructs an object from the Weather Underground JSON data.
        """

        template = (
            # (field, wufield, converter)
            ('station_id', 'station_id', unicode),
            ('observation', 'observation_time_rfc822', lambda x: strptimez(x, RFC822_DATETIME)),
            ('weather', 'weather', unicode),
            ('temp', 'temperature_string', unicode),
            ('temp_cels', 'temp_c', float),
            ('temp_fahr', 'temp_f', float),
            ('wind', 'wind_string', unicode),
            ('wind_dir', 'wind_dir', unicode),
            ('wind_degree', 'wind_degrees', int),
            ('wind_mph', 'wind_mph', float),
            ('wind_gust_mph', 'wind_gust_mph', float),
            ('pressure', 'pressure_mb', int),
            ('dewpoint', 'dewpoint_string', unicode),
            ('precipitation', 'precip_today_string', unicode),
            ('icon', 'icon', unicode),
        )

        kwargs = {}
        for field, wufield, converter in template:
            kwargs[field] = converter(data.get(wufield, u''))
        return klass(**kwargs)
