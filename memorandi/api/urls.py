# memorandi.api.urls
# URL Endpoints for the JSON RESTful API
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Feb 12 00:00:07 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: urls.py [] benjamin@bengfort.com $

"""
URL Endpoints for the JSON RESTful API
"""

##########################################################################
## Imports
##########################################################################

from api import views
from rest_framework import routers
from django.conf.urls import patterns, include, url

##########################################################################
## ViewSet Routers
##########################################################################

# Declare API Endpoints
endpoints = (
    (r'locations', views.LocationViewSet),
    (r'weather', views.WeatherViewSet),
    (r'journal', views.JournalViewSet),
    (r'profile', views.ProfileViewSet),
    (r'author', views.AuthorViewSet),
)

# Create Router from Endpoints
router = routers.DefaultRouter()
for endpoint in endpoints:
    router.register(*endpoint)

##########################################################################
## Endpoints
##########################################################################

urlpatterns = patterns('',
    # Defined Endpoints from Router
    url(r'^', include(router.urls)),

    # API Authentication
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
)
