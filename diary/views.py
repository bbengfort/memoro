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

from django.http import Http404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class TodayView(LoginRequiredMixin, UpdateView):

    model = Memo
    form_class = TodayForm
    template_name = "site/today.html"

    def form_valid(self, form):
        """
        Add some message input that the form has been successfully saved.
        """
        rep = super(TodayView, self).form_valid(form)
        messages.add_message(
            self.request,
            messages.INFO,
            f"Entry for {form.instance} successfully updated"
        )
        return rep

    def get_success_url(self):
        """
        Send the user back to the today view.
        """
        return reverse_lazy("today")

    def get_object(self, queryset=None):
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
        context = super(TodayView, self).get_context_data(**kwargs)
        context['page'] = 'today'
        context['locations'] = Location.objects.filter(quick_select=True)
        context['feelings'] = FEELINGS
        return context


class CalendarView(LoginRequiredMixin, ListView):

    model = Memo
    template_name = "site/calendar.html"

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the view.
        """
        context = super(CalendarView, self).get_context_data(**kwargs)
        context['page'] = 'calendar'
        return context


class EntryView(LoginRequiredMixin, DetailView):

    model = Memo
    template_name = "site/entry.html"

    def get_object(self, queryset=None):
        """
        Returns the Memo entry by date.
        """
        if queryset is None:
            queryset = self.get_queryset()

        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        if not year or not month or not day:
            raise AttributeError(
                "entry view not called with enough date components for lookup"
            )

        try:
            day = date(year, month, day)
            return queryset.get(date=day, author=self.request.user)
        except queryset.model.DoesNotExist:
            raise Http404(_("No entry found for this date and author"))

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the view.
        """
        context = super(EntryView, self).get_context_data(**kwargs)
        context['page'] = 'calendar'
        return context