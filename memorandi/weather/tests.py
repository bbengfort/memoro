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

import unittest

from .wunder import *
from .models import *
from .managers import *
from utils.timez import now
from urlparse import urljoin
from location.models import *
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

    def test_init_override(self):
        """
        Ensure Wunder instances can accept apikey
        """
        options = {'API_KEY': 'almostarealkey'}
        with self.settings(WEATHER_UNDERGROUND=options):
            try:
                wunder = Wunder(apikey='notarealkey')
            except ImproperlyConfigured:
                self.fail("ImproperlyConfigured raised in error.")
            self.assertNotEqual(wunder.apikey, settings.WEATHER_UNDERGROUND.get('API_KEY'))

    def test_environment(self):
        """
        Ensure that a test wunder api key is available
        """
        self.assertTrue(hasattr(settings, 'WEATHER_UNDERGROUND'))
        self.assertIn('API_KEY', settings.WEATHER_UNDERGROUND)
        self.assertTrue(settings.WEATHER_UNDERGROUND['API_KEY'])

    def test_urlbase(self):
        """
        Assert that the urlbase is correctly joined
        """
        assumed = "http://api.wunderground.com/api/123456/"
        with self.settings(WEATHER_UNDERGROUND={'API_KEY': '123456'}):
            wunder = Wunder()
            self.assertEqual(assumed, wunder.urlbase)

    def test_single_feature_endpoint(self):
        """
        Test endpoint construction of single feature
        """
        assumed = "http://api.wunderground.com/api/123456/astronomy/q/"
        with self.settings(WEATHER_UNDERGROUND={'API_KEY': '123456'}):
            wunder   = Wunder()
            endpoint = wunder.get_features_endpoint('astronomy')
            self.assertEqual(assumed, endpoint)

    def test_multiple_feature_endpoint(self):
        """
        Test endpoint construction of multiple features
        """
        assumed = "http://api.wunderground.com/api/123456/astronomy/conditions/q/"
        with self.settings(WEATHER_UNDERGROUND={'API_KEY': '123456'}):
            wunder   = Wunder()
            endpoint = wunder.get_features_endpoint('astronomy', 'conditions')
            self.assertEqual(assumed, endpoint)

    def test_invalid_feature(self):
        """
        Check invalid feature won't report
        """
        with self.assertRaises(NotImplementedError):
            wunder = Wunder()
            wunder.get_features_endpoint('unknownasd12342')

    def test_query_endpoint(self):
        """
        Test endpoint construction of a query
        """
        assumed = "http://api.wunderground.com/api/123456/astronomy/q/CA/San_Francisco.json"
        with self.settings(WEATHER_UNDERGROUND={'API_KEY': '123456'}):
            wunder   = Wunder()
            endpoint = wunder.get_query_endpoint('CA/San_Francisco', 'astronomy')
            self.assertEqual(assumed, endpoint)

    def test_fetch_weather(self):
        """
        Actually attempt to fetch weather from the API!
        """
        wunder   = Wunder()
        response = wunder.fetch_weather("DC/Washington")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

class WeatherManagerTests(TestCase):
    """
    Tests the Weather Manager
    """

    fixtures = ['landmarks.json',]

    @unittest.expectedFailure
    def test_current_weather(self):
        """
        Test get or create functionality of manager

        This test needs to be corrected- the API is doing strange thing.
        (e.g. this test fails some of the time, and it's not obvious what
        is causing the failure, or how to reproduce the error)
        """
        location = Location.objects.get(pk=1)

        # Check that weather is fetched via the API
        weather, created = Weather.objects.current_weather(location)
        self.assertTrue(weather)
        self.assertTrue(created)

        # Check that the weather is fetched from the Database
        weather, created = Weather.objects.current_weather(location)
        self.assertTrue(weather)
        self.assertFalse(created)

    def test_hour_range_now(self):
        """
        Check the hour range functionality
        """
        rng = hour_range()
        self.assertLess(rng[0], now())
        self.assertGreater(rng[1], now())
