# memorandi.api.views
# Viewsets for the RESTful API
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Feb 12 00:04:43 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Viewsets for the RESTful API
"""

##########################################################################
## Imports
##########################################################################

from location.models import Location
from weather.models import Weather
from narrate.models import Memorandum
from rest_framework import viewsets
from location.serializers import *
from weather.serializers import *
from narrate.serializers import *

from rest_framework.decorators import link, action
from rest_framework.response import Response

##########################################################################
## API Viewsets
##########################################################################

class LocationViewSet(viewsets.ModelViewSet):

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class WeatherViewSet(viewsets.ModelViewSet):

    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer

class JournalViewSet(viewsets.ModelViewSet):

    queryset = Memorandum.objects.all()
    serializer_class = MemorandumSerializer
