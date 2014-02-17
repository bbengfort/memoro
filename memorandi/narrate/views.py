# memorandi.narrate.views
# These are the main app views to serve web content
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Mon Feb 17 08:16:29 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
These are the main app views to serve web content
"""

##########################################################################
## Imports
##########################################################################

from django.shortcuts import redirect
from authors.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

##########################################################################
## Application Views
##########################################################################

class SplashPage(TemplateView):
    """
    Main splash page for the app. Although this is essentially a simple
    webpage with no need for extra context, this view does check if the
    user is logged in, and if so, immediately redirects them to the app.
    """

    template_name = "site/index.html"

    def dispatch(self, request, *args, **kwargs):
        """
        If user is authenticated, redirect to Application, otherwise serve
        normal template view as expected.
        """
        if request.user.is_authenticated():
            return redirect('app-root', permanent=False)
        return super(SplashPage, self).dispatch(request, *args, **kwargs)

class WebAppView(LoginRequiredMixin, TemplateView):
    """
    Authenticated web application view that serves all context and content
    to kick off the Backbone front-end application.
    """

    template_name = "app/index.html"
