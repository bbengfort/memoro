# memorandi.authors.urls
# URL Routers for the accounts endpoint
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Feb 15 20:39:59 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: urls.py [] benjamin@bengfort.com $

"""
URL Routers for the accounts endpoint
"""

##########################################################################
## Imports
##########################################################################

from .views import *
from django.conf.urls import patterns, url

##########################################################################
## Patterns
##########################################################################

urlpatterns = patterns('',
    url(r'login/$', LoginView.as_view(), name=LoginView.__name__),
    url(r'logout/$', LogoutView.as_view(), name=LogoutView.__name__),
    url(r'profile/$', ProfileView.as_view(), name=ProfileView.__name__),
    url(r'password/$', ChangePasswordView.as_view(), name=ChangePasswordView.__name__),
    url(r'password/reset/$', PasswordResetView.as_view(), name=PasswordResetView.__name__),
    url(r'password/reset/done/$', PasswordResetDoneView.as_view(), name=PasswordResetDoneView.__name__),
    url(r'password/reset/confirm/(?P<uidb36>\w{1,13})-(?P<token>\w{1,13}-\w{1,20})/$', PasswordResetConfirmView.as_view(), name=PasswordResetConfirmView.__name__),
    url(r'password/reset/complete/$', PasswordResetCompleteView.as_view(), name=PasswordResetCompleteView.__name__),
)
