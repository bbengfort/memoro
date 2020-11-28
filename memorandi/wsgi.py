
# memorandi.wsgi
# WSGI config for memorandi project.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Nov 28 13:44:01 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: wsgi.py [] benjamin@bengfort.com $

"""
WSGI config for memorandi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

##########################################################################
## Imports
##########################################################################

import os

from django.core.wsgi import get_wsgi_application
from dotenv import find_dotenv, load_dotenv


##########################################################################
## Load environment and create WSGI application
##########################################################################

load_dotenv(find_dotenv())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memorandi.settings')
application = get_wsgi_application()
