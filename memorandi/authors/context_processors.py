# memorandi.authors.context_processors
# Template context processors extending the auth processor
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Feb 15 21:37:24 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: context_processors.py [] benjamin@bengfort.com $

"""
Template context processors extending the auth processor
"""

##########################################################################
## Imports
##########################################################################

from .models import Author

##########################################################################
## Processors
##########################################################################

def author(request):
    if hasattr(request, 'author'):
        return {
            'author': author,
        }
    return {}