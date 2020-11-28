# memorandi.asgi
# ASGI config for memorandi project.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Nov 28 13:44:01 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: asgi.py [] benjamin@bengfort.com $

"""
ASGI config for memorandi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""


##########################################################################
## Imports
##########################################################################

import os

from django.core.asgi import get_asgi_application
from dotenv import find_dotenv, load_dotenv


##########################################################################
## Load environment and create ASGI application
##########################################################################

load_dotenv(find_dotenv())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memorandi.settings')
application = get_asgi_application()