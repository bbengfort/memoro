# diary.forms
# Form classes for interacting with model objects.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Dec 02 19:20:23 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: forms.py [] benjamin@bengfort.com $

"""
Form classes for interacting with model objects.
"""

##########################################################################
## Imports
##########################################################################

from django import forms
from diary.models import Memo


##########################################################################
## Forms
##########################################################################

class TodayForm(forms.ModelForm):

    desktop_windows = forms.IntegerField(required=False)
    desktop_tabs = forms.IntegerField(required=False)
    mobile_tabs = forms.IntegerField(required=False)
    tablet_tabs = forms.IntegerField(required=False)

    class Meta:
        model = Memo
        fields = [
            "memo", "entry", "private", "feeling", "location",
            "desktop_windows", "desktop_tabs", "mobile_tabs", "tablet_tabs",
        ]

