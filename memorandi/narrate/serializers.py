# memorandi.narrate.serializers
# Serialize the default models of the Narrate app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Feb 12 00:12:50 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
Serialize the default models of the Narrate app
"""

##########################################################################
## Imports
##########################################################################

from .models import *
from rest_framework import serializers

##########################################################################
## Serializers
##########################################################################

class MemorandumSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model  = Memorandum
        fields = ('id', 'url', 'title', 'body')
