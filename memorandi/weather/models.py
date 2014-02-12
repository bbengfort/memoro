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
from model_utils.models import TimeStampedModel

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
    observation = models.CharField( max_length=255, **nullable )   # The time string of observation
    weather     = models.CharField( max_length=255, **nullable )   # Description of the weather
    temp        = models.CharField( max_length=255, **nullable )   # Textual description of temperature
    temp_cels   = models.FloatField( **nullable )  # Temperature in degrees Celsius
    temp_fahr   = models.FloatField( **nullable )  # Temperature in degrees Fahrenheit
    wind        = models.CharField( max_length=255, **nullable )   # Description of the wind
    wind_dir    = models.CharField( max_length=255, **nullable )   # Compass direction of the wind
    wind_degree = models.FloatField( **nullable )    # Degree of wind direction
    wind_mph    = models.FloatField( **nullable )    # Speed of wind in MPH
    wind_gust_mph = models.FloatField( **nullable )  # Gust speed of wind in MPH
    pressure    = models.IntegerField( **nullable )  # Pressure in millibars
    dewpoint    = models.CharField( max_length=255, **nullable )   # Textual Description of Dewpoint
    precipitation = models.CharField( max_length=255, **nullable ) # Textual Description of Precipitation
    icon        = models.CharField( max_length=255, **nullable )   # Icon of weather

    class Meta:
        db_table        = "weather"
        verbose_name    = "weather"
        unique_together = ("station_id", "observation")
        verbose_name_plural = "weather"

    def __unicode__(self):
        return "%s on %s" % (self.weather, self.observation)
