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
from django.core.exceptions import ObjectDoesNotExist

from diary.models import Memo, Tabs


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

    def save(self):
        """
        Saves the related objects to Today's memo in along with the form.
        """
        # Save the form data before moving on to other fields
        super(TodayForm, self).save()

        # Save the tabs one to one model
        tabs_fields = ["desktop_windows", "desktop_tabs", "mobile_tabs", "tablet_tabs"]
        tabs_data = {
            field: self.cleaned_data[field]
            for field in tabs_fields
            if self.cleaned_data[field] is not None
        }

        if tabs_data:
            try:
                for name, attr in tabs_data.items():
                    setattr(self.instance.tabs, name, attr)
                self.instance.tabs.save()
            except ObjectDoesNotExist:
                Tabs.objects.create(memo=self.instance, **tabs_data)

