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

##########################################################################
## Location Managers
##########################################################################

class GeographyManager(models.Manager):
    """
    Helper functions for GeoEntity queries.
    """

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
