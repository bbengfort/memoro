# reading.management.commands.instapaper
# CLI interface to Instapaper API
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Jan 01 14:37:36 2021 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: instapaper.py [] benjamin@bengfort.com $

"""
CLI interface to Instapaper API
"""

##########################################################################
## Imports
##########################################################################

import os
import getpass

from datetime import date
from diary.models import Memo
from reading.instapaper import Instapaper
from django.contrib.auth.models import User
from reading.utils import parse_bool, parse_timestamp
from reading.instapaper import InstapaperException, HTTPException
from django.core.management.base import BaseCommand, CommandError
from reading.models import Article, ArticleCounts, InstapaperAccount


##########################################################################
## Command
##########################################################################

class Command(BaseCommand):

    help = "synchronzize Instapaper reading list"

    def add_arguments(self, parser):
        parser.add_argument(
            "-D", "--debug", action="store_true",
            help="print detailed information about exceptions"
        )
        parser.add_argument(
            "-u", "--username", metavar="USER",
            default=os.getenv("INSTAPAPER_USERNAME"),
            help="Instapaper username to authenticate with via OAuth",
        )
        parser.add_argument(
            "-p", "--password", metavar="PASS",
            default=os.getenv("INSTAPAPER_PASSWORD"),
            help="Instapaper password to authenticate with via OAuth",
        )
        parser.add_argument(
            "-U", "--user", metavar="USER", default=getpass.getuser(),
            help="Memoro username to associate Instapaper account with",
        )
        parser.add_argument(
            "-a", "--associate", action="store_true",
            help="associate local articles with memoro entries without api call"
        )
        parser.add_argument(
            "-c", "--article-count", action="store_true",
            help="perform the article count for today's memoro"
        )

    def handle(self, *args, **options):
        # Get the user associated with the account
        self.get_user(options["user"])

        if options["associate"]:
            self.associate()
            return

        if options["article_count"]:
            self.article_count()
            return

        with http_error(options["debug"]):
            # Create the Instapaper API client, using cached access tokens if available.
            self.make_instapaper_client(**options)

            # Note: ignoring the "starred" folder since this duplicates other folders
            # TODO: handle other folders
            for folder in ("unread", "archive"):
                # Get the have query to reduce the result set returned
                have = Article.instapaper.have(self.user, folder)
                bookmarks = self.client.bookmarks(
                    limit=500, folder_id=folder, have=have
                )

                # Handle bookmarks and report the results
                crt, upd, dlt = self.handle_bookmarks(bookmarks, folder)
                print(f"{crt} created, {upd} updated, {dlt} deleted in {folder}")

    def get_user(self, username):
        try:
            self.user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"{username} is not a valid memoro user")

        # Ensure the user has an associated instapaper account
        if not hasattr(self.user, "instapaper_account"):
            InstapaperAccount.objects.create(user=self.user)

    def make_instapaper_client(self, **options):
        # Get cached access credentials if they exist
        account = self.user.instapaper_account
        if account.oauth_token and account.oauth_token_secret:
            self.client = Instapaper.cached_access_token(
                account.oauth_token, account.oauth_token_secret
            )

            try:
                # Attempt to verify the credentials if not, force reauthenticate
                self.verify_credentials(account)
                # The cached credentials are working - continue!
                return
            except InstapaperException:
                # Don't do anything if there is an error to reauthenticate
                pass

        # Create the Instapaper API client
        self.client = Instapaper()
        token = self.client.authenticate(options["username"], options["password"])
        account.refresh_from_api(token)
        account.save()

        # Verify the credentials to make sure access is working
        self.verify_credentials(account)

    def verify_credentials(self, account):
        # Verify credentials and update instapaper account
        creds = self.client.verify_credentials()
        for item in creds:
            if item["type"] == "user":
                account.refresh_from_api(item)
                account.save()

    def handle_bookmarks(self, bookmarks, folder):
        """
        Updates the database with the fetched bookmarks
        """
        account = self.user.instapaper_account
        created, updated, deleted = 0, 0, 0

        for record in bookmarks:
            rtype = record.pop("type").lower().strip()
            if rtype == "bookmark":
                if Article.instapaper.from_bookmark(account, record, folder):
                    created += 1
                else:
                    updated += 1

            elif rtype == "user":
                account.refresh_from_api(record)
                account.save()

            elif rtype == "meta":
                deleted_ids = record.get("delete_ids", None)
                if deleted_ids:
                    deleted += Article.instapaper.delete_bookmarks(deleted_ids)

            else:
                raise ValueError(f"unhandled record type '{rtype}'")

        return created, updated, deleted

    def associate(self):
        # Go through all articles in any folder that don't have a memo to associate.
        query = Article.objects.filter(account=self.user.instapaper_account)
        query = query.order_by('-progress_timestamp')

        count = 0
        for article in query:
            if not article.read():
                article.memo = None
                article.save()
                continue

            memo = Memo.objects.filter(date=article.progress_timestamp.date()).first()
            if memo:
                article.memo = memo
                article.save()
                count += 1

        print(f"associated {count} articles")

    def article_count(self):
        counts = ArticleCounts.objects.daily_counts(self.user.instapaper_account)

        print(counts)
        print(f"year to date: {counts.archived} archived, {counts.starred} starred")


class http_error(object):

    def __init__(self, debug):
        self.debug = debug

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        if value is None:
            return True

        if etype == HTTPException:
            if self.debug:
                print(e.response)
                print(e.body)
                return False
            raise CommandError(str(value)) from value

        if etype == InstapaperException:
            if self.debug:
                return False
            raise CommandError(str(value)) from value

        return False
