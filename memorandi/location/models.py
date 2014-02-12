# memorandi.location.models
# Models for the location metadata
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Feb 11 14:41:06 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Models for the location metadata
"""

##########################################################################
## Imports
##########################################################################

from utils import nullable
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel

##########################################################################
## Models
##########################################################################

class Location(TimeStampedModel):
    """
    A generic wrapper class that embeds location meta data into the memos.
    Note that a location can be very generic (including a completely null
    location). There are some constraints on uniqueness in the meta, but
    this data type should be handled well.

    Note that I chose not to use the Django contrib GeoDjango package for
    spatial data. I felt that this was WAY too much information. However,
    I believe the data types stored in this model can be used to leverage
    GIS data in the future.
    """

    name         = models.CharField( max_length=255, **nullable ) # A place name, e.g. "Home"
    address      = models.CharField( max_length=255, **nullable ) # A specific address
    city         = models.CharField( max_length=255, **nullable ) # Name of the city
    country      = models.ForeignKey( "GeoEntity", related_name="+", **nullable )   # Country GeoEntity
    region       = models.ForeignKey( "GeoEntity", related_name="+", **nullable )   # Region GeoEntity
    latitude     = models.FloatField( **nullable )                # Decimal latitude
    longitude    = models.FloatField( **nullable )                # Decimal longitude
    postal_code  = models.CharField( max_length=31 )              # Postal code
    ipaddr       = models.IPAddressField( **nullable )            # IP Address of request

    class Meta:
        db_table        = "location"
        verbose_name    = "location"
        unique_together = (
            ("latitude", "longitude"),
            ("name", "address", "city", "country", "region", "postal_code"),
        )
        verbose_name_plural = "locations"

    def __unicode__(self):
        if self.name:
            return "%s in %s, %s" % (self.name, self.city, self.region.iso_code)
        return "%s, %s" % (self.city, self.region)

class GeoEntity(TimeStampedModel):
    """
    A database of geographic entities, e.g. regions or countries that have
    ISO codes and common names associated with them in different languages.

    This is simply for ease of data storage and lookups on location table.
    Technically, if leveraging the parent- any Geographic Entity can be
    referenced through the smallest entity (the region) and then all other
    data can be grabbed upwards. However, it's nice to have a reference to
    the country and the region in the location model.
    """

    TYPES        = Choices(
        (0, "continent", "Continent"),
        (1, "country", "Country"),
        (2, "region", "Region"),
    )

    name         = models.CharField( max_length=255 ) # Name of the region or country
    iso_code     = models.CharField( max_length=3 )   # ISO Code for the region or country
    region_type  = models.PositiveSmallIntegerField( choices=TYPES, default=TYPES.country ) # Type of Geographic Region
    parent       = models.ForeignKey( "GeoEntity", related_name="+", **nullable )           # Regions specify country as parent

    class Meta:
        db_table        = "geographic_entity"
        verbose_name    = "geographic entity"
        unique_together = ("name", "iso_code", "region_type")
        verbose_name_plural = "geographic entities"

    def __unicode__(self):
        return self.name
