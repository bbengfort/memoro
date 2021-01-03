# reading.forms
# Web forms for simple HTTP interactions
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Jan 02 11:08:37 2021 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: forms.py [] benjamin@bengfort.com $

"""
Web forms for simple HTTP interactions
"""

##########################################################################
## Imports
##########################################################################

from django import forms
from reading.instapaper import Instapaper
from reading.models import Article, ArticleCounts
from django.core.exceptions import ValidationError


##########################################################################
## Instapaper Login Form
##########################################################################

class InstapaperLoginForm(forms.Form):

    username = forms.CharField(required=False)
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    oauth_cached = forms.BooleanField(required=False)

    def __init__(self, account, **kwargs):
        # Create the initial data from the account
        # NOTE: currently using a custom form that doesn't use initial values
        # TODO: update Instapaper manager view to use initial values
        initial = kwargs.get("initial", {})
        initial["oauth_cached"] = account.has_cached_oauth()
        initial["email"] = account.username
        kwargs["initial"] = initial

        # Instantiate the form
        super(InstapaperLoginForm, self).__init__(**kwargs)

        # Save the account data on the form for processing
        self.account = account
        self.client = None

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        oauth_cached = cleaned_data.get("oauth_cached")

        if oauth_cached and not self.account.has_cached_oauth():
            raise ValidationError(
                "oauth cached specified but account does not have access token"
            )

        if not oauth_cached:
            if not username:
                self.add_error("username", "username required without access token")

            if not password:
                self.add_error("password", "password required without access token")

        return self.cleaned_data

    def authenticate(self):
        """
        This method creates an Instapaper API client either from the supplied
        credentials or from the access token cached in the account, then verifies
        the credentials of the user.
        """
        if self.cleaned_data["oauth_cached"]:
            # Create client from tokens
            self.client = Instapaper.cached_access_token(
                self.account.oauth_token, self.account.oauth_token_secret
            )

        else:
            # Create the client from the username and password
            # Authenticate and save the OAuth tokens to the account
            self.client = Instapaper()
            token = self.client.authenticate(
                self.cleaned_data["username"], self.cleaned_data["password"]
            )
            self.account.refresh_from_api(token)
            self.account.save()

        # Verify credentials
        # TODO: if OAuth tokens have expired give feedback to user to reauthenticate
        creds = self.client.verify_credentials()
        for item in creds:
            if item["type"] == "user":
                self.account.refresh_from_api(item)
                self.account.save()

    def synchronize(self):
        """
        This method performs a "daily synchronization" - it fetches bookmarks from
        Instapaper and updates all bookmarks with their reading progress. It then
        creates a daily article count for today if there is a Memo.
        """
        if self.client is None:
            raise ValidationError("cannot synchronize without authentication")

        # Return update statistics across all folders
        created, updated, deleted = 0, 0, 0

        # NOTE: ignoring "starred" folder since this duplicates other folders
        # TODO: handle other folders created by the user
        for folder in ("unread", "archive"):
            # Use the have parameter to reduce the result set returned
            have = Article.instapaper.have(self.account, folder)
            bookmarks = self.client.bookmarks(limit=500, folder_id=folder, have=have)

            for record in bookmarks:
                rtype = record.pop("type").lower().strip()
                if rtype == "bookmark":
                    if Article.instapaper.from_bookmark(self.account, record, folder):
                        created += 1
                    else:
                        updated += 1

                elif rtype == "user":
                    self.account.refresh_from_api(record)
                    self.account.save()

                elif rtype == "meta":
                    deleted_ids = record.get("delted_ids", None)
                    if deleted_ids:
                        deleted += Article.instapaper.delete_bookmarks(deleted_ids)

                else:
                    raise ValueError(f"unhandled record type '{rtype}'")

        # Create daily counts for Memoro
        ArticleCounts.objects.daily_counts(self.account)

        # Return the number of API interactions that occurred
        return created, updated, deleted