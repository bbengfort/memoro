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
