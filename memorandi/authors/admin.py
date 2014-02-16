# memorandi.authors.admin
# Register models with the admin
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Feb 15 20:32:37 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Register models with the admin
"""

from .models import Profile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

##########################################################################
## Admin classes and Inlines
##########################################################################

class ProfileInline(admin.StackedInline):

    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(UserAdmin):

    inlines = (ProfileInline,)

##########################################################################
## Admin Registration
##########################################################################

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
