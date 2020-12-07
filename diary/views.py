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

from calendar import Calendar
from datetime import date, timedelta

from diary.forms import TodayForm
from diary.models import Location, GeoEntity
from diary.models import Memo, FEELINGS, Tabs

from django.http import Http404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView
from django.core.exceptions import SuspiciousOperation
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
    calendar = Calendar(firstweekday=6)
    template_name = "site/calendar.html"

    def get_queryset(self):
        """
        Filter entries by currently logged in user.
        """
        queryset = super(CalendarView, self).get_queryset()
        queryset = queryset.filter(author=self.request.user)

        month = self.get_month()
        return queryset.filter(date__month=month.month, date__year=month.year)

    def get_month(self):
        """
        Get the month requested from the query string using today as defaults
        """
        try:
            today = date.today()
            month = int(self.request.GET.get("month", today.month))
            year = int(self.request.GET.get("year", today.year))
            return date(year, month, 1)
        except ValueError:
            raise SuspiciousOperation("bad date query parameters")

    def get_weeks(self):
        """
        Gets the weeks and days for the current month, populating with query data.
        """
        entries = {}
        for day in self.get_queryset().values('date'):
            day = day['date']
            entries[day] = reverse_lazy(
                'entry',
                kwargs=dict(zip(('year', 'month', 'day'), (day.year, day.month, day.day)))
            )

        month = self.get_month()
        weeks = []
        for week in self.calendar.monthdatescalendar(month.year, month.month):
            week_data = []
            for day in week:
                if day.month == month.month:
                    week_data.append(
                        (day, entries.get(day, None))
                    )
                else:
                    week_data.append((None, None))
            weeks.append(week_data)
        return weeks

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the view.
        """
        context = super(CalendarView, self).get_context_data(**kwargs)
        context['page'] = 'calendar'
        context['weeks'] = self.get_weeks()
        context['month'] = self.get_month()
        context['today'] = date.today()
        context['prev_month'] = (context['month'] - timedelta(days=1)).replace(day=1)
        context['next_month'] = (context['month'] + timedelta(days=32)).replace(day=1)
        return context


class EntryView(LoginRequiredMixin, DetailView):

    model = Memo
    template_name = "site/entry.html"

    def get_queryset(self):
        """
        Filter entries by currently logged in user.
        """
        queryset = super(EntryView, self).get_queryset()
        return queryset.filter(author=self.request.user)

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
            return queryset.get(date=day)
        except queryset.model.DoesNotExist:
            raise Http404(_("No entry found for this date and author"))

    def get_nav_entries(self, obj):
        """
        Returns the (prev, next) entries in the database if they exist.
        """
        queryset = self.get_queryset()
        prev = queryset.order_by('-date').filter(date__lt=obj.date).first()
        next = queryset.order_by('date').filter(date__gt=obj.date).first()
        return prev, next

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the view.
        """
        context = super(EntryView, self).get_context_data(**kwargs)
        context['page'] = 'calendar'

        obj = context['object']
        context['prev_entry'], context['next_entry'] = self.get_nav_entries(obj)
        return context