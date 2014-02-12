# memorandi.location.serializers
# Serialize the default models of the Location app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Feb 12 00:31:21 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
Serialize the default models of the Location app
"""

##########################################################################
## Imports
##########################################################################

from .models import *
from rest_framework import serializers

##########################################################################
## Serializers
##########################################################################

class LocationSerializer(serializers.HyperlinkedModelSerializer):

    region  = serializers.RelatedField(source="region")
    country = serializers.RelatedField(source="country")

    class Meta:
        model  = Location
        fields = ('id', 'url', 'name', 'address', 'city', 'region',
                  'country', 'postal_code', 'latitude', 'longitude', 'ipaddr')
