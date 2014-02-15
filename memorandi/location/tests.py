# memorandi.location.tests
# Testing location specific code
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Feb 14 19:43:12 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: tests.py [] benjamin@bengfort.com $

"""
Testing location specific code
"""

##########################################################################
## Imports
##########################################################################

import unittest

from .models import *
from django.test import TestCase

##########################################################################
## Model Test Cases
##########################################################################

class LocationModelTests(TestCase):
    """
    Testing the location model
    """

    fixtures = ['landmarks.json',]

    def test_unicode(self):
        """
        Check the intense unicode method
        """

        runs = (
            u"Home in Washington, DC",
            u"DCA",
            u"(38.921618, -77.011506)",
            u"Poilane in Paris, France",
            u"21045",
        )

        for idx, val in enumerate(runs):
            self.assertEqual(unicode(Location.objects.get(pk=(idx+1))), val)

    def test_to_query(self):
        """
        Check the weather underground query string
        """
        runs = (
            u"pws:KDCWASHI18",   # Should we check State/City for U.S. locations?
            u"DCA",
            u"38.921618,-77.011506",
            u"France/Paris",
            u"21045",
        )
        for idx, val in enumerate(runs):
            self.assertEqual(Location.objects.get(pk=idx+1).to_query(), val)

    @unittest.expectedFailure
    def test_geoip_import(self):
        """
        Check if GeoIP2 library is able to be imported
        """
        try:
            import geoip2.database as geoip
        except ImportError as e:
            self.fail("Could not import GeoIP2: %s" % str(e))

##########################################################################
## Manager Test Cases
##########################################################################

class GeographyManagerTests(TestCase):
    """
    Testing the location manager
    """

    def test_USA(self):
        """
        Assert you can grab USA easily
        """
        USA = GeoEntity.objects.USA
        self.assertTrue(USA)
        self.assertEqual(USA.iso_code, "US")
        self.assertEqual(USA.name, "United States")

    def test_states(self):
        """
        Assert states are accessible
        """
        self.assertEqual(GeoEntity.objects.states().count(), 59)

    def test_continents(self):
        """
        Assert continents are accessible
        """
        self.assertEqual(GeoEntity.objects.continents().count(), 7)

    def test_countries(self):
        """
        Assert countries are accessible
        """
        self.assertEqual(GeoEntity.objects.countries().count(), 249)
