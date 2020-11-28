# memoro.settings.testing
# Configuration for testing and continuous integration.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Nov 28 16:40:07 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: testing.py [] benjamin@bengfort.com $

"""
Configuration for testing and continuous integration.
"""

##########################################################################
## Imports
##########################################################################

import pathlib
import tempfile
import dj_database_url

from .base import *  # noqa
from .base import DATABASES


##########################################################################
## Test Settings
##########################################################################

# Temporary Directory
TESTDIR = pathlib.Path(tempfile.TemporaryDirectory(prefix="memoro_test_").name)

# Hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Specify the name of the test database
DATABASES['default']['TEST'] = {'NAME': 'memoro_test'}

# Content without side effects
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
MEDIA_ROOT = TESTDIR / "media"
STATIC_ROOT = TESTDIR / "static"
