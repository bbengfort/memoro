# memorandi.narrate.urls
# URL router for views in the application
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Mon Feb 17 08:26:50 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: urls.py [] benjamin@bengfort.com $

"""
URL router for views in the application.

Handles all the views in the narrate app with the exception of the main
SplashPage view, which is added to the main URLs controller.
"""

##########################################################################
## Imports
##########################################################################

from .views import *
from django.conf.urls import patterns, url

##########################################################################
## Patterns
##########################################################################

urlpatterns = patterns('',
    url(r'^$', WebAppView.as_view(), name="app-root"),
    url(r'^write/$', WriteView.as_view(), name="app-write"),
)
