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

from datetime import date

from diary.forms import TodayForm
from diary.models import Location, GeoEntity
from diary.models import Memo, FEELINGS, Tabs

from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class Today(LoginRequiredMixin, UpdateView):

    model = Memo
    form_class = TodayForm
    template_name = "site/today.html"

    def get_success_url(self):
        """
        Send the user back to the today view.
        """
        return reverse_lazy("today")

    def get_object(self):
        """
        Gets or creates today's memo for editing. The memo is created as soon as the
        site is accessed for the first time. Note that access to the request is needed
        to get the currently logged in user to create the memo for.
        """
        obj, _ = Memo.objects.get_or_create(date=date.today(), author=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the view.
        """
        context = super(Today, self).get_context_data(**kwargs)
        context['page'] = 'today'
        context['locations'] = Location.objects.filter(quick_select=True)
        context['feelings'] = FEELINGS
        return context
