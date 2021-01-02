# reading.managers
# Database managers for reading objecs
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Jan 01 18:06:52 2021 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: managers.py [] benjamin@bengfort.com $

"""
Database managers for reading objecs
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from django.apps import apps
from django.contrib.auth import get_user_model


##########################################################################
## Articles Manager and Queryset
##########################################################################

class InstapaperQueryset(models.QuerySet):

    def have(self):
        """
        Returns the "have" parameter of the bookmarks API method, a comma-separated
        string of "bookmark_id:hash" pairs for the current queryset. This method does
        not provide any additional filtering.
        """
        return ",".join([
            f"{row[0]}:{row[1]}"
            for row in self.values_list("bookmark_id", "hash")
        ])


class InstapaperManager(models.Manager):

    def get_queryset(self):
        return InstapaperQueryset(self.model, using=self._db)

    def have(self, account, folder="unread"):
        """
        Returns the "have" parameter of the bookmarks API method: a comma-separated
        string of "bookmark_id:hash" pairs. This method additionally filters on a
        specific user/account and folder and only returns articles that haven't been
        deleted. If different filters are required, use the queryset directly.
        """
        if isinstance(account, get_user_model()):
            if not hasattr(account, "instapaper_account"):
                InstapaperAccount = apps.get_model("reading", "InstapaperAccount")
                account = InstapaperAccount.objects.create(user=account)
            else:
                account = account.instapaper_account

        query = self.filter(account=account, folder=folder, deleted=False)
        return query.have()