# memorandi.authors.serializers
# Serializes objects in the Authors app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Feb 15 21:43:16 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
Serializes objects in the Authors app
"""

##########################################################################
## Imports
##########################################################################

from .models import Profile, Author
from rest_framework import serializers
from location.serializers import LocationSerializer

##########################################################################
## Serializers
##########################################################################

class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    location   = LocationSerializer(source='location')

    class Meta:
        model  = Profile
        fields = ('id', 'url', 'birthday', 'anniversary', 'twitter',
                  'website', 'tagline', 'prompt', 'location')

class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    profile    = ProfileSerializer(source='profile')

    class Meta:
        model  = Author
        fields = ('id', 'url', 'username', 'first_name', 'last_name', 'email')
        lookup_field = 'username'
