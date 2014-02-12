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
## Markdown Field
##########################################################################

class MarkdownField(serializers.WritableField):

    def to_native(self, obj):
        """
        This is a good enough hack for now, but will need to do something
        better about it in the future. The error when not utilizing this
        method of serialization is:

            'unicode' object has no attribute 'raw'

        Relating to the attempt to call the field `raw` propertery but it
        has already been passed as a unicode string.
        """
        return unicode(obj)

##########################################################################
## Serializers
##########################################################################

class MemorandumSerializer(serializers.HyperlinkedModelSerializer):

    body   = MarkdownField()
    author = serializers.PrimaryKeyRelatedField()

    class Meta:
        model  = Memorandum
        lookup_field = "slug"
        fields = ('id', 'url', 'title', 'body', 'author')
