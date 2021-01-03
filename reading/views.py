# reading.views
# Views and request handlers for the reading app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Jan 01 09:01:03 2021 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views and request handlers for the reading app
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import messages
from reading.forms import InstapaperLoginForm
from django.views.generic.edit import FormView
from reading.instapaper import InstapaperException
from reading.models import InstapaperAccount, Article
from django.contrib.auth.mixins import LoginRequiredMixin


class InstapaperManager(LoginRequiredMixin, FormView):
    """
    Allows manual interaction to update Memoro with Instapaper records.
    """

    form_class = InstapaperLoginForm
    template_name = "site/instapaper.html"
    success_url = "/instapaper/"

    def form_valid(self, form):
        try:
            form.authenticate()
        except InstapaperException as e:
            form.add_error(None, f"authentication failed ({e})")
            return self.form_invalid(form)

        try:
            msg = "{0} created, {1} updated, {2} deleted".format(*form.synchronize())
            messages.success(self.request, msg)
        except InstapaperException as e:
            form.add_error(None, f"synchronization failed ({e})")
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_form_kwargs(self):
        """
        Add the account to the form kwargs
        """
        kwargs = super(InstapaperManager, self).get_form_kwargs()

        if not hasattr(self.request.user, "instapaper_account"):
            InstapaperAccount.objects.create(user=self.request.user)

        kwargs["account"] = self.request.user.instapaper_account
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Ensure that the authenticated user has an Instapaper account.
        """
        context = super(InstapaperManager, self).get_context_data(**kwargs)
        context['page'] = 'instapaper'

        # Add article context
        articles = Article.instapaper.account(self.request.user.instapaper_account)
        context['article_counts'] = {
            "read": articles.read().count(),
            "unread": articles.unread().count(),
            "archived": articles.archived().count(),
            "starred": articles.starred().count(),
        }

        return context
