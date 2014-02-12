# memorandi.memorandi.urls
# URL Endpoints for the Memorandi Project
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Feb 12 00:10:24 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: urls.py [] benjamin@bengfort.com $

"""
URL Endpoints for the Memorandi Project
"""

##########################################################################
## Imports
##########################################################################

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Admin Autodiscover
from django.contrib import admin
admin.autodiscover()

##########################################################################
## URL Patterns
##########################################################################

urlpatterns = patterns('',
    # Application URLs
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),

    # API Endpoints
    url(r'^api/', include('api.urls'), name='api'),

    # Styled Admin
    url(r'^admin/', include(admin.site.urls)),
)
