# diary.views
# Views control the logic of request handling.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Dec 02 13:14:57 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views control the logic of request handling.
"""

##########################################################################
## Imports
##########################################################################

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class Today(LoginRequiredMixin, TemplateView):

    template_name = "site/today.html"

    def get_context_data(self, **kwargs):
        context = super(Today, self).get_context_data(**kwargs)
        context['page'] = 'today'
        return context
