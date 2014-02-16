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
