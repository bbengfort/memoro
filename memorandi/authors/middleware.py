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

##########################################################################
## Middleware
##########################################################################

class AuthorMiddleware(object):
    """
    Adds the author proxy to the context from the user object.
    """

    def process_request(self, request):
        try:
            request.author = Author.fromUser(request.user)
        except:
            request.author = None
        return None
