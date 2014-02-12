# memorandi.api.tests
# Tests for the Memorandi API
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Feb 12 09:45:02 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: tests.py [] benjamin@bengfort.com $

"""
Tests for the Memorandi API
"""

##########################################################################
## Imports
##########################################################################

from rest_framework import status
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

##########################################################################
## Test Cases
##########################################################################

class JournalTests(APITestCase):

    def setUp(self):
        self.list_endpoint = reverse('memorandum-list')
        self.test_user     = User.objects.create_user('tester', password='secret')
        self.client.login(username='tester', password='secret')

    def test_create_with_author(self):
        """
        Ensure journal entry creation with specified author
        """
        url  = self.list_endpoint
        data = {
            'title': 'A test entry',
            'body': 'To journal or not to journal, _that_ is the question.',
            'author': 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], 1)

    def test_create_without_author(self):
        """
        Ensure that journal entry is created with current author
        """
        url  = self.list_endpoint
        data = {
            'title': 'A test entry',
            'body': 'To journal or not to journal, _that_ is the question.',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['author'])

    def test_create_markdown(self):
        """
        Assert markdown is rendered in HTML
        """
        url  = self.list_endpoint
        data = {
            'title': 'A test entry',
            'body': 'To journal or not to journal, _that_ is the question.',
            'author': 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = u'<p>To journal or not to journal, <em>that</em> is the question.</p>'
        self.assertEqual(response.data['body'], body)

    def test_delete(self):
        """
        Ensure entries can be deleted via API
        """
        url  = self.list_endpoint
        data = {
            'title': 'A test entry',
            'body': 'To journal or not to journal, _that_ is the question.',
            'author': 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(response.data['url'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authentication(self):
        """
        Assert authentication is required for POST
        """
        url  = self.list_endpoint
        data = {
            'title': 'A test entry',
            'body': 'To journal or not to journal, _that_ is the question.',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.delete(response.data['url'])
        self.client.logout()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
