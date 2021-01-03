# reading.utils
# Helper functions for the reading app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Jan 01 18:46:20 2021 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: utils.py [] benjamin@bengfort.com $

"""
Helper functions for the reading app
"""

##########################################################################
## Imports
##########################################################################

import oauth2
import httplib2

from datetime import datetime, timezone


##########################################################################
## Parsing helpers
##########################################################################

def parse_bool(val):
    """
    Attempt to convert an environment variable into a boolean. Recommend using True or
    False as the boolean values but can also use 1 or 0.
    """
    if isinstance(val, str):
        # Try true/false strings
        if val.lower().startswith('f'):
            return False
        if val.lower().startswith('t'):
            return True

        # Try integer strings
        val = int(val)
    return bool(val)


def parse_timestamp(val):
    """
    Convert a unix timestamp into a timezone-aware datetime object
    """
    return datetime.fromtimestamp(int(val), tz=timezone.utc)
