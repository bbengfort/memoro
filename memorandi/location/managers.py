# memorandi.location.managers
# Manager classes to handle location queries
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Feb 14 18:21:03 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: managers.py [] benjamin@bengfort.com $

"""
Manager classes to handle location queries
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
import geoip2.database as geoip
from django.conf import settings

##########################################################################
## Location Managers
##########################################################################

class LocationManager(models.Manager):
    """
    Helper functions for Location including geoip creation
    """

    def create_ipaddr(self, addr, mmdb=None):
        """
        Creates a location with an IP address
        """
        mmdb   = mmdb or settings.GEOIP2_CITY
        reader = geoip.Reader(mmdb)
        result = reader.city(addr)
        record = self.model.from_mmdb(result)
        record.save(force_insert=True)
        return record

    def geoip(self, addr, mmdb=None):
        """
        Get or create a record for an IP address. Returns a tuple of the
        found object and a boolean if it was created or not (just like the
        get_or_create method normally would).
        """
        try:
            return self.get(ipaddr=addr), False
        except self.model.DoesNotExist:
            return self.create_ipaddr(addr, mmdb), True

class GeographyManager(models.Manager):
    """
    Helper functions for GeoEntity queries.
    """

    def iso_code(self, iso_code):
        """
        Shortcut for:
            self.get_or_create(iso_code=iso_code)[0]
        """
        return self.get_or_create(iso_code=iso_code)[0]

    @property
    def USA(self):
        """
        Returns the USA country entity.
        """
        return self.get(iso_code="US")

    def states(self):
        """
        Returns the list of U.S. States
        """
        return self.regions(self.USA)

    def continents(self):
        return self.filter(region_type=self.model.TYPES.continent)

    def countries(self):
        """
        TODO: filter for a particular continent.
        """
        return self.filter(region_type=self.model.TYPES.country)

    def regions(self, country=None):
        """
        Return regions, optionally filtering for a particular country.
        """
        query = self.filter(region_type=self.model.TYPES.region)
        if country:
            query = query.filter(parent=country)
        return query
