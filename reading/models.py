# reading.models
# Database models for the reading app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Jan 01 09:01:03 2021 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: models.py [] benjamin@bengfort.com $

"""
Database models for the reading app
"""

##########################################################################
## Imports
##########################################################################

import warnings

from django.db import models
from django.conf import settings
from reading.utils import parse_bool
from model_utils.models import TimeStampedModel
from reading.managers import InstapaperManager, ArticleCountsManager


##########################################################################
## Article Models
##########################################################################

class Article(TimeStampedModel):
    """
    An Article is something that has been read, usually on the web that we want to save
    a history of for later. The most common way to add read articles is to save them to
    Instapaper and read them there. Alternatively, they can be generated from URLs.

    This record is specialized for web articles and blogs. Magazine articles, scientific
    papers, etc will require different models stored in Memoro.
    """

    url = models.URLField(
        null=True, blank=True, default=None, max_length=500,
        help_text="The source of the article (will be empty if private source isn't)",
    )

    title = models.CharField(
        max_length=512, null=True, blank=True, default=None,
        help_text="The title of the article"
    )

    description = models.CharField(
        max_length=2000, null=True, blank=True, default=None,
        help_text="A brief description or summary of the article"
    )

    hash = models.CharField(
        max_length=60, blank=True, null=True, default=None,
        help_text="The Instapaper metadata hash for change detection"
    )

    progress = models.FloatField(
        null=True, blank=True, default=None,
        help_text="The percentage of the article read so far between 0 and 1"
    )

    progress_timestamp = models.DateTimeField(
        null=True, blank=True, default=None,
        help_text="The timestamp the progress was updated on"
    )

    bookmark_id = models.IntegerField(
        null=True, blank=True, default=None,
        help_text="The Instapaper bookmark id"
    )

    private_source = models.CharField(
        max_length=255, null=True, blank=True, default=None,
        help_text="The Instapaper private source (if stored, no URL is stored)"
    )

    time = models.DateTimeField(
        null=True, blank=True, default=None,
        help_text="Instapaper time field, likely when it was created or added"
    )

    starred = models.BooleanField(
        default=False, help_text="If the article has been starred in Instapaper"
    )

    folder = models.CharField(
        max_length=128, default="unread", blank=True, null=False,
        help_text="The Instapaper folder id, unread, starred, or archive"
    )

    memo = models.ForeignKey(
        "diary.Memo", models.SET_NULL, null=True, blank=True, related_name="articles",
        help_text="The memo the article is associated with, usually the day read"
    )

    deleted = models.BooleanField(
        default=False, help_text="If the article was deleted in Instapaper"
    )

    account = models.ForeignKey(
        "reading.InstapaperAccount", models.PROTECT,
        null=False, blank=False, related_name="bookmarks",
        help_text="The Instapaper account that fetched the article/bookmark"
    )

    class Meta:
        db_table = "web_articles"
        ordering = ("-progress_timestamp",)
        get_latest_by = "progress_timestamp"
        verbose_name = "Web Article"
        verbose_name_plural = "Web Articles"
        unique_together = ("url", "private_source")

    # Managers
    objects = models.Manager()
    instapaper = InstapaperManager()

    def __str__(self):
        if self.title:
            return self.title
        if self.private_source:
            return self.private_source
        return self.url

    def read(self):
        """
        Detects if the article has been read based on the progress fields.
        """
        # NOTE: apparently the progress goes back to 0.0 when the article has been
        # read 100% in some cases; so if the article is not in the unread folder,
        # I've also added a check if progress is later than time, meaning that some
        # progress has been made.
        if self.progress > 0.0:
            return True
        return (self.folder != "unread" and self.progress_timestamp > self.time)


##########################################################################
## Article Counts
##########################################################################

class ArticleCounts(TimeStampedModel):
    """
    Records reading progress for a specific day.
    """

    memo = models.OneToOneField(
        "diary.Memo", models.CASCADE,
        null=False, blank=False, related_name="article_counts",
        help_text="The reading list counts for the specified day",
    )

    read = models.PositiveSmallIntegerField(
        default=None, null=True, blank=True,
        help_text="The number of articles read today"
    )

    unread = models.PositiveSmallIntegerField(
        default=None, null=True, blank=True,
        help_text="The number of articles to read today"
    )

    archived = models.PositiveSmallIntegerField(
        default=None, null=True, blank=True,
        help_text="The number of articles archived, year to date"
    )

    starred = models.PositiveSmallIntegerField(
        default=None, null=True, blank=True,
        help_text="The number of articles starred, year to date"
    )

    class Meta:
        db_table = "article_counts"
        verbose_name = "Reading List Count"
        verbose_name_plural = "Reading List Counts"
        ordering = ("-memo__date",)
        get_latest_by = "memo__date"

    objects = ArticleCountsManager()

    def __str__(self):
        return f"{self.read} read today, {self.unread} still unread"


##########################################################################
## Instapaper Access Token Cache
##########################################################################

class InstapaperAccount(TimeStampedModel):
    """
    Contains instapaper user information as well as cached OAuth access tokens.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, models.CASCADE,
        null=False, blank=False, related_name="instapaper_account",
        help_text="The memoro user associated with the instapaper account"
    )

    account_id = models.IntegerField(
        null=True, blank=True, default=None,
        help_text="The Instapaper user_id field (should not change)"
    )

    username = models.CharField(
        null=True, blank=True, default=None, max_length=255,
        help_text="The Instapaper username field (may change)"
    )

    subscription_is_active = models.BooleanField(
        null=True, default=None, blank=True,
        help_text="If the account is using Instapaper Premium or not"
    )

    oauth_token = models.CharField(
        max_length=75, null=True, blank=True, default=None, editable=False,
        help_text="Cached xAuth token from authentication"
    )

    oauth_token_secret = models.CharField(
        max_length=75, null=True, blank=True, default=None, editable=False,
        help_text="Cached xAuth secret from authentication"
    )

    class Meta:
        db_table = "instapaper_accounts"
        ordering = ("-modified",)
        get_latest_by = "modified"
        verbose_name = "Instapaper Account"
        verbose_name_plural = "Instapaper Accounts"

    def __str__(self):
        if self.username:
            return self.username
        return str(self.user)

    def has_cached_oauth(self):
        return bool(self.oauth_token and self.oauth_token_secret)

    def refresh_from_api(self, data, check_unhandled=True):
        """
        Updates account information from data response from API.
        """
        # Handle special fields
        self.account_id = data.get("user_id", self.account_id)
        self.subscription_is_active = parse_bool(
            data.get("subscription_is_active", self.subscription_is_active)
        )

        # Handle matching fields
        for field in ("username", "oauth_token", "oauth_token_secret"):
            if field in data and data[field]:
                setattr(self, field, data[field])

        if check_unhandled:
            known_fields = {
                "user_id", "subscription_is_active", "username",
                "oauth_token", "oauth_token_secret", "type"
            }
            for field in data:
                if field not in known_fields:
                    warnings.warn(
                        f"unhandled instapaper account field from API '{field}'"
                    )
