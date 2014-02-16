# memorandi.authors.models
# Models for extended profiles and Author proxy
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Feb 15 20:22:24 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Models for extended profiles and Author proxy
"""

##########################################################################
## Imports
##########################################################################

import urllib
import hashlib

from utils import nullable
from django.db import models
from model_utils import Choices
from django.contrib.auth.models import User

##########################################################################
## Helper methods
##########################################################################

def get_gravatar_url(email, size=120, default="mm"):
    """
    Constructs the gravatar URL for an email address.
    """
    digest  = hashlib.md5(email.lower()).hexdigest()
    params  = urllib.urlencode({'d':default, 's':str(size)})
    gravurl = "http://www.gravatar.com/avatar/%s?%s" % (digest, params)
    return gravurl

##########################################################################
## Profile model to extend Django user with more information
##########################################################################

class Profile(models.Model):

    user        = models.OneToOneField( 'auth.User', editable=False, related_name="profile" )
    birthday    = models.DateField( **nullable )
    anniversary = models.DateField( **nullable )
    twitter     = models.CharField( max_length=100, **nullable )
    website     = models.URLField( **nullable )
    tagline     = models.CharField( max_length=255, **nullable )
    prompt      = models.TextField( **nullable )
    location    = models.ForeignKey( 'location.Location', related_name="+", **nullable)

    @property
    def gravatar(self):
        return get_gravatar_url(self.user.email)

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def full_email(self):
        email = "%s <%s>" % (self.full_name, self.user.email)
        return email.strip()

    def delete(self, using=None):
        self.user.delete(using=using)
        super(UserProfile, self).delete(using=using)

    def __unicode__(self):
        return self.full_email

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        db_table = "auth_profile"

##########################################################################
## Django User Model Proxy
##########################################################################

class Author(User):
    """
    Proxy class for django.contrib.auth.models.User for enacting our
    methods and management on the User database without affecting the
    User class.
    """

    #objects = AuthorManager()

    @classmethod
    def fromUser(klass, user):
        return klass.objects.get(pk=user.pk)

    @property
    def gravatar(self):
        return get_gravatar_url(self.user.email)

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def full_email(self):
        return self.get_profile().full_email

    def __unicode__(self):
        return self.full_name

    class Meta:
        proxy= True
