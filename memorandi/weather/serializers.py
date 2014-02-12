# memorandi.weather.serializers
# Serialize the default models of the Weather app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Feb 12 00:31:21 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
Serialize the default models of the Weather app
"""

##########################################################################
## Imports
##########################################################################

from .models import *
from rest_framework import serializers

##########################################################################
## Serializers
##########################################################################

class WeatherSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model  = Weather
