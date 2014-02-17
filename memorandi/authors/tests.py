# memorandi.authors.tests
# Test the Authors app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  timestamp
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: tests.py [] benjamin@bengfort.com $

"""
Test the Authors app
"""

##########################################################################
## Imports
##########################################################################

from django.test import TestCase
from .models import Profile, Author
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

##########################################################################
## Test Cases
##########################################################################

class AuthorsModelTest(TestCase):

    def test_user_post_save_profile(self):
        """
        Ensure a profile is created on User save.
        """

        # Create a user
        user = User.objects.create_user('test', 'test@example.com', 's3cr3t')

        # Assert that a profile exists for the user
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_proxy_post_save_profile(self):
        """
        Ensure a profile is created on User Proxy save.
        """
        # Create an Author
        user = Author.objects.create_user('test', 'test@example.com', 's3cr3t')

        # Assert that a profile exists for the user
        self.assertTrue(Profile.objects.filter(user=user).exists())

class AuthorContextProcessorTest(TestCase):

    def test_author_in_context(self):
        """
        Assert context has an author
        """
        user = Author.objects.create_user('test', 'test@example.com', 's3cr3t')
        self.client.login(username='test', password='s3cr3t')
        response = self.client.get(reverse('app-root'))

        self.assertIn('author', response.context)
        self.assertEqual(response.context['author'], user)

    def test_ipaddr_in_context(self):
        """
        Assert context has an IP address
        """
        response = self.client.get('/')
        self.assertIn('ipaddr', response.context)
