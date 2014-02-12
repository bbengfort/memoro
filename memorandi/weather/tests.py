# memorandi.weather.tests
# Testing the weather app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Feb 12 11:09:02 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: tests.py [] benjamin@bengfort.com $

"""
Testing the weather app
"""

##########################################################################
## Imports
##########################################################################

from .wunder import *
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

##########################################################################
## Test Cases
##########################################################################

class WunderTests(TestCase):
    """
    Tests the wunder module.
    """

    def test_api_key_configured(self):
        """
        Assert no API KEY raises configuration exception
        """
        with self.assertRaises(ImproperlyConfigured):
            with self.settings(WEATHER_UNDERGROUND={}):
                wunder = Wunder()

    def test_environment(self):
        """
        Ensure that a test wunder api key is available
        """
        self.assertTrue(hasattr(settings, 'WEATHER_UNDERGROUND'))
        self.assertIn('API_KEY', settings.WEATHER_UNDERGROUND)
        self.assertTrue(settings.WEATHER_UNDERGROUND['API_KEY'])
