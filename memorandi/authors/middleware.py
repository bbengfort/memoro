# memorandi.authors.middleware
# Request middleware to help with author management
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Feb 15 21:41:20 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: middleware.py [] benjamin@bengfort.com $

"""
Request middleware to help with author management
"""

##########################################################################
## Imports
##########################################################################

from .models import Author
from ipware.ip import get_real_ip

##########################################################################
## Helper functions
##########################################################################

def result_or_none(func):
    """
    Captures exceptions and returns None if that happens.
    """
    try:
        return func()
    except:
        return None

##########################################################################
## Middleware
##########################################################################

class AuthorMiddleware(object):
    """
    Adds the author proxy to the context from the user object.
    """

    def process_request(self, request):
        request.author = result_or_none(lambda: Author.fromUser(request.user))
        request.ipaddr = result_or_none(lambda: get_real_ip(request))
        return None
