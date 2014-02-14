# memorandi.utils.timez
# Time utilities for ensuring that the Timezone is properly handled.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Nov 07 09:18:13 2013 -0500
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: timez.py [] benjamin@bengfort.com $

"""
Time utilities for ensuring that the Timezone is properly handled.
"""

##########################################################################
## Imports
##########################################################################

import re

from dateutil.tz import tzlocal, tzutc
from datetime import datetime, timedelta

##########################################################################
## Format constants
##########################################################################

HUMAN_DATETIME   = "%a %b %d %H:%M:%S %Y %z"
HUMAN_DATE       = "%b %d, %Y"
HUMAN_TIME       = "%I:%M:%S %p"
JSON_DATETIME    = "%Y-%m-%dT%H:%M:%S.%fZ" # Must be UTC
RFC822_DATETIME  = "%a, %d %b %Y %H:%M:%S %z"
ISO8601_DATETIME = "%Y-%m-%dT%H:%M:%S%z"
ISO8601_DATE     = "%Y-%m-%d"
ISO8601_TIME     = "%H:%M:%S"
COMMON_DATETIME  = "%d/%b/%Y:%H:%M:%S %z"

##########################################################################
## Module helper function
##########################################################################

zre = re.compile(r'([\-\+]\d{4})')
def strptimez(dtstr, dtfmt):
    """
    Helper function that performs the timezone calculation to correctly
    compute the '%z' format that is not added by default in Python 2.7.
    """
    if '%z' not in dtfmt:
        return datetime.strptime(dtstr, dtfmt)

    dtfmt  = dtfmt.replace('%z', '')
    offset = int(zre.search(dtstr).group(1))
    dtstr  = zre.sub('', dtstr)
    delta  = timedelta(hours = offset/100)
    utctsp = datetime.strptime(dtstr, dtfmt) - delta
    return utctsp.replace(tzinfo=tzutc())

def now(local=False):
    """
    Returns a timezone aware datetime object.
    """
    if local:
        return Clock.localnow()
    return Clock.utcnow()

##########################################################################
## Clock Module
##########################################################################

class Clock(object):
    """
    A time serializer that wraps local and utc time collection and
    maintains knowledge of how to format the times for particular uses.
    Intended usage is as follows:

        >>> clock = Clock("json", local=False) # UTC JSON formatter
        >>> print clock
        2013-11-07T14:35:16.611224Z
        >>> time.sleep(30)
        >>> print clock
        2013-11-07T14:35:46.611661Z

    """

    FORMATS = {
        "long":    HUMAN_DATETIME,
        "json":    JSON_DATETIME,
        "short":   HUMAN_DATE,
        "clock":   HUMAN_TIME,
        "iso8601": ISO8601_DATETIME,
        "iso":     ISO8601_DATETIME,
        "isodate": ISO8601_DATE,
        "isotime": ISO8601_TIME,
        "human":   HUMAN_DATETIME,
        "common":  COMMON_DATETIME,
        "apache":  COMMON_DATETIME,
    }

    @staticmethod
    def localnow():
        return datetime.now(tzlocal())

    @staticmethod
    def utcnow():
        now = datetime.utcnow()
        now = now.replace(tzinfo=tzutc())
        return now

    def __init__(self, default="long", local=False, formats={}):
        self.formats = self.FORMATS.copy()
        self.formats.update(formats)
        self.default_format = default.lower().replace('-', '').replace('_', '')
        self.use_local = local

    def format(self, dt, fmt=None):
        fmt = fmt or self.default_format
        if fmt in self.formats:
            fmt = self.formats[fmt]
        return dt.strftime(fmt)

    def strfnow(self, fmt=None):
        nowdt  = self.localnow() if self.use_local else self.utcnow()
        return self.format(nowdt, fmt)

    def __str__(self):
        return self.strfnow()

if __name__ == '__main__':
    import time
    clock = Clock("human", local=True)  # UTC JSON clock formatter
    print clock
    time.sleep(30)
    print clock
