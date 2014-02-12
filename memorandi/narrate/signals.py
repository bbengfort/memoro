# memorandi.narrate.signals
# Hooks for database signals
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Feb 11 21:16:13 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: signals.py [] benjamin@bengfort.com $

"""
Hooks for database signals
"""

##########################################################################
## Imports
##########################################################################

from django.utils.text import slugify

##########################################################################
## Signal Functions
##########################################################################

def create_slug(sender, instance, **kwargs):
    """
    When a memorandum is created, also update slugfield
    """
    if not instance.slug:
        date = instance.created.strftime('%Y %m %d')
        slug = "%s %s" % (date, instance.title)
        instance.slug = slugify(slug)
