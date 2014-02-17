# memorandi.narrate.tests
# Unit Tests for the Narrate App
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Feb 11 23:06:51 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: tests.py [] benjamin@bengfort.com $

"""
Unit Tests for the Narrate App
"""

##########################################################################
## Imports
##########################################################################

from .models import *
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

##########################################################################
## Model Test Cases
##########################################################################

class MemorandumModelTest(TestCase):

    def test_slug_on_save(self):
        """
        Ensure that Memorandum models get a slug on save.
        """
        kwargs = {
            "title": u"Test Memo",
            "body": u"This is a note that I'm adding to my journal.",
            "author": User.objects.get(username='benjamin')
        }
        memo = Memorandum.objects.create(**kwargs)
        self.assertIsNotNone(memo.slug)

##########################################################################
## View Test Cases
##########################################################################

class NarrateViewsTest(TestCase):

    def test_splash_page_redirect(self):
        """
        Ensure authenticated users are redirected to app
        """
        self.test_user = User.objects.create_user('tester', password='secret')
        self.client.login(username='tester', password='secret')
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('app-root'))

    def test_splash_page(self):
        """
        Ensure unauthenticated users are not redirected
        """
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'site/index.html')

    def test_app_login_required(self):
        """
        Assert that access to any view in the app requires login
        """

        # List of views that should be protected
        protected = (
            'api-root',
        )
        msg = "View '%s' responded to unauthenticated user."

        for name in protected:
            self.client.logout()  # Ensure we're logged out
            url = reverse(name)   # Get the url for this view
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403, msg % name)
