# memorandi.narrate.models
# Models for the Narrative portion of Memorandi
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Feb 11 20:49:43 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Models for the Narrative portion of Memorandi
"""

##########################################################################
## Imports
##########################################################################

from utils import nullable
from django.db import models
from model_utils import Choices
from .signals import create_slug
from django.db.models import signals
from markupfield.fields import MarkupField
from taggit.managers import TaggableManager
from model_utils.models import TimeStampedModel

##########################################################################
## Models
##########################################################################

class Memorandum(TimeStampedModel):

    title    = models.CharField( max_length=100 )                   # The title of the entry
    slug     = models.SlugField( max_length=128, unique=True, editable=False )  # A slug of the title for the entry
    body     = MarkupField( markup_type="markdown" )                # The actual entry itself, in Markdown
    author   = models.ForeignKey( 'auth.User' )                     # The author of the entry
    location = models.ForeignKey( 'location.Location', **nullable ) # Where the entry was written
    weather  = models.ForeignKey( 'weather.Weather', **nullable )   # The weather at the time of the entry

    tags     = TaggableManager( blank=True )

    class Meta:
        db_table     = "journal"
        verbose_name = "memorandum"
        verbose_name_plural = "memoranda"

    def __unicode__(self):
        return "%s on %s" % (self.title, self.created.strftime("%d %b %Y"))

######################################################################
## Register Signals on the Models
######################################################################

signals.pre_save.connect(create_slug, sender=Memorandum)
