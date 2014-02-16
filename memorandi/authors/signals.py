# memorandi.authors.signals
# Hooks for database signals
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Feb 15 20:31:48 2014 -0500
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

from .models import Profile, Author
from django.db.models import signals
from django.contrib.auth.models import User

##########################################################################
## Signals methods
##########################################################################

def create_profile(sender, instance, signal, created, **kwargs):
    """
    When a user is created, also create a matching profile.
    If raw is set, this is being loaded from a fixture, so ignore.
    """
    if created and not kwargs.get('raw', False):
        Profile(user=instance).save()

######################################################################
## Ensure that when a Student or User is created, a Profile is too.
######################################################################

signals.post_save.connect(create_profile, sender=User)
signals.post_save.connect(create_profile, sender=Author)
