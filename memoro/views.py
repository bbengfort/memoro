# memoro.views
# Default application views for the memoro project.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Nov 28 17:10:31 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: views.py [] benjamin@bengfort.com $

"""
Default application views for the memoro project, especially views that aren't
necessarily associated with a specific app such as the home page or status endpoints.
"""

##########################################################################
## Imports
##########################################################################

from datetime import datetime
from memoro.version import get_version, get_revision

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


##########################################################################
## Web Views
##########################################################################

class Overview(LoginRequiredMixin, TemplateView):

    template_name = "site/overview.html"


##########################################################################
## API Views
##########################################################################

class HeartbeatViewSet(viewsets.ViewSet):
    """
    Endpoint for heartbeat checking, includes status and version.
    """

    permission_classes = [AllowAny]

    def list(self, request):
        return Response({
            "status": "ok",
            "version": get_version(),
            "revision": get_revision(short=True),
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        })


##########################################################################
## Error Views
##########################################################################

def server_error(request, **kwargs):
    return render(request, template_name='errors/500.html', status=500)


def not_found(request, exception, **kwargs):
    return render(request, template_name='errors/404.html', status=404)


def permission_denied(request, exception, **kwargs):
    return render(request, template_name='errors/403.html', status=403)


def bad_request(request, exception, **kwargs):
    return render(request, template_name='errors/400.html', status=400)