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

from datetime import date
from django.db import models
from django.apps import apps
from django.contrib.auth import get_user_model
from reading.utils import parse_bool, parse_timestamp


##########################################################################
## Articles Manager and Queryset
##########################################################################

class InstapaperQueryset(models.QuerySet):

    def have(self):
        """
        Returns the "have" parameter of the bookmarks API method, a comma-separated
        string of "bookmark_id:hash" pairs for the current queryset. This method does
        not provide any additional filtering - but it is recommended to filter deleted
        articles before running this query.
        """
        return ",".join([
            f"{row[0]}:{row[1]}"
            for row in self.values_list("bookmark_id", "hash")
        ])

    def read(self):
        return self.filter(memo__isnull=False)

    def unread(self):
        return self.filter(folder="unread", memo__isnull=True)

    def archived(self):
        return self.filter(folder="archive")

    def starred(self):
        return self.filter(starred=True)

    def ytd(self, year=None):
        """
        Returns all articles whose Instapaper time is this year.
        """
        if year is None:
            year = date.today().year
        return self.filter(time__year=year)

    def account(self, account, active_only=True):
        """
        Filter by account or user. If active_only is True - filters deleted.
        """
        if isinstance(account, get_user_model()):
            if not hasattr(account, "instapaper_account"):
                InstapaperAccount = apps.get_model("reading", "InstapaperAccount")
                account = InstapaperAccount.objects.create(user=account)
            else:
                account = account.instapaper_account

        if active_only:
            return self.filter(account=account, deleted=False)
        return self.filter(account=account)


class InstapaperManager(models.Manager):

    def get_queryset(self):
        return InstapaperQueryset(self.model, using=self._db)

    def from_bookmark(self, account, record, folder="unread"):
        """
        Create or updates an article from a bookmark record returned from the API.
        """
        # Add account and folder information
        record["folder"] = folder
        record["account"] = account

        # Parse the record into the model format
        bookmark_id = record.pop("bookmark_id")
        record["time"] = parse_timestamp(record["time"])
        record["starred"] = parse_bool(record["starred"])
        record["progress_timestamp"] = parse_timestamp(record["progress_timestamp"])

        # If record has been moved it will be marked "deleted" from a previous folder,
        # so if we're updating a bookmark from the API we must ensure that it is not
        # marked as deleted since we know it's in Instapaper.
        record["deleted"] = False

        # Update or create the bookmark
        article, created = self.update_or_create(
            bookmark_id=bookmark_id, defaults=record
        )

        # Associate the article with Memoro if the reading progress is greater than 0
        # based on the day of the progress timestamp. If progress increases on multiple
        # days, this will cause the last day to be the Memoro record.
        if article.read():
            Memo = apps.get_model("diary", "Memo")
            memo = Memo.objects.filter(date=article.progress_timestamp.date()).first()
            if memo:
                article.memo = memo
                article.save()

        # Return if the bookmark was created or updated
        return created

    def delete_bookmarks(self, deleted_ids):
        """
        Soft delete articles based on the deleted_ids parameter from the Instapaper API.
        """
        # Deleted IDs could be an empty string, just ignore in this case
        if not deleted_ids:
            return 0

        deleted = 0
        for bookmark_id in deleted_ids.split(","):
            bookmark_id = int(bookmark_id.strip())
            article = self.filter(bookmark_id=bookmark_id).first()
            if article:
                article.deleted = True
                article.save()
                deleted += 1

        return deleted

    def have(self, account, folder="unread"):
        """
        Returns the "have" parameter of the bookmarks API method: a comma-separated
        string of "bookmark_id:hash" pairs. This method additionally filters on a
        specific user/account and folder and only returns articles that haven't been
        deleted. If different filters are required, use the queryset directly.
        """
        query = self.get_queryset()
        query = query.account(account=account, active_only=True).filter(folder=folder)
        return query.have()

    def read(self):
        return self.get_queryset().read()

    def unread(self):
        return self.get_queryset().unread()

    def archived(self):
        return self.get_queryset().archived()

    def starred(self):
        return self.get_queryset().starred()

    def ytd(self, year=None):
        """
        Returns all articles whose Instapaper time is this year.
        """
        return self.get_queryset().ytd(year=year)

    def account(self, account, active_only=True):
        """
        Filter by account or user. If active_only is True - filters deleted.
        """
        return self.get_queryset().account(account=account, active_only=True)


##########################################################################
## Article Counts Manager
##########################################################################

class ArticleCountsManager(models.Manager):

    def daily_counts(self, account):
        """
        Creates or updates the daily counts for a Memo object.
        """
        Memo = apps.get_model("diary", "Memo")
        memo = Memo.objects.filter(date=date.today(), author=account.user).first()

        # If there is no memo object, we cannot create the daily_counts - no error
        if not memo:
            return

        # Associate the article counts with the memo
        if not hasattr(memo, "article_counts"):
            counts = self.create(memo=memo)
        else:
            counts = memo.article_counts

        # Compute the number of articles read today
        counts.read = memo.articles.count()

        # Create a queryset for the instapaper account
        Article = apps.get_model("reading", "Article")
        qs = Article.instapaper.account(account)

        # Add the current unread count for today
        counts.unread = qs.unread().count()

        # Filter for year to date counts
        qs = qs.ytd(memo.date.year)
        counts.archived= qs.archived().count()
        counts.starred = qs.starred().count()
        counts.save()

        return counts