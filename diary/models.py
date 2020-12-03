# diary.models
# Database model definitions.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Dec 02 13:14:57 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: models.py [] benjamin@bengfort.com $

"""
Database model definitions.
"""

##########################################################################
## Imports
##########################################################################

import re

from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _

from datetime import date
from model_utils import Choices
from model_utils.models import TimeStampedModel


_RE_WHITESPACE = re.compile(r"\s+")


##########################################################################
## Enumerations
##########################################################################

FEELINGS = Choices(
    (-2, "terrible", _("terrible")),
    (-1, "poor", _("poor")),
    (-0, "fair", _("fair")),
    (1, "good", _("good")),
    (2, "excellent", _("excellent")),
)


##########################################################################
## Models
##########################################################################

class Memo(TimeStampedModel):
    """
    A Memo represents a single diary entry for a specific day. It is the primary unit
    of work in memoro and most other objects are attached to a specific daily memo.
    """

    date = models.DateField(
        null=False, blank=False, default=date.today, unique=True,
        help_text="Date of the diary entry"
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.PROTECT,
        null=False, blank=False, related_name="memos",
        help_text="The author of the diary entry"
    )

    memo = models.CharField(
        null=True, blank=True, default=None, max_length=255,
        help_text="A brief description of the day, e.g. the highlights"
    )

    entry = models.TextField(
        null=True, blank=True, default=None,
        help_text="The diary entry for the day (in Markdown)"
    )

    private = models.BooleanField(
        default=False,
        help_text="If the entry contains sensitive or private information"
    )

    feeling = models.SmallIntegerField(
        null=False, blank=True, default=FEELINGS.fair, choices=FEELINGS,
        help_text="A Likert scale of your general feeling about the day",
    )

    location = models.ForeignKey(
        "diary.Location", models.SET_NULL,
        null=True, blank=True, related_name="memos",
        help_text="The location where the diary entry was written",
    )

    class Meta:
        db_table = "memos"
        ordering = ("-date",)
        get_latest_by = "date"
        verbose_name = "Memorandum"
        verbose_name_plural = "Memoranda"

    def __str__(self):
        return self.date.strftime("%A %B %d, %Y")


class Location(TimeStampedModel):
    """
    Specifies a geographic location by latitude/longitude coordinates and optionally
    by an address or a name for quick reference.
    """

    name = models.CharField(
        max_length=255, null=True, blank=True, default=None,
        help_text="A place name e.g. Home or Work"
    )

    latitude = models.FloatField(
        null=True, blank=True, default=None,
        help_text="Decimal latitude of the location"
    )

    longitude = models.FloatField(
        null=True, blank=True, default=None,
        help_text="Decimal longitude of the location"
    )

    ipaddr = models.GenericIPAddressField(
        null=True, blank=True, default=None,
        help_text="The originating IP address of the location"
    )

    address = models.CharField(
        max_length=255, null=True, blank=True, default=None,
        help_text="A specific address on a single line"
    )

    city = models.CharField(
        max_length=255, null=True, blank=True, default=None,
        help_text="Name of the city specified by the address"
    )

    country = models.ForeignKey(
        "diary.GeoEntity", models.PROTECT, related_name="+", null=True, blank=True, default=None,
        help_text="Entity representing the Country of the address"
    )

    region = models.ForeignKey(
        "diary.GeoEntity", models.PROTECT, related_name="+", null=True, blank=True, default=None,
        help_text="Entity representing the Region, Province, or State of the address"
    )

    postal_code = models.CharField(
        max_length=31, null=True, blank=True, default=None,
        help_text="Postal code of the address or other coded identification"
    )

    quick_select = models.BooleanField(
        default=False,
        help_text="Allow this location to appear in quick select forms"
    )

    class Meta:
        db_table = "locations"
        ordering = ("-modified",)
        get_latest_by = "modified"
        unique_together = (
            ("name", "latitude", "longitude"),
            ("name", "address", "city", "country", "region", "postal_code"),
        )
        verbose_name = "location"
        verbose_name_plural = "locations"

    def __str__(self):
        if self.name:
            return self.name

        addr = f"{self.address} {self.city} {self.region} {self.postal_code} {self.country}"
        addr = _RE_WHITESPACE.sub(" ", addr).strip()
        if addr:
            return addr

        if self.latitude and self.longitude:
            return f"({self.latitude}, {self.longitude})"

        if self.ipaddr:
            return self.ipaddr

        return "<Empty>"


class GeoEntity(TimeStampedModel):
    """
    A database of geographic entries, e.g. regions or countries that have ISO codes and
    common names associated with them in different languages. Intended to provide ease
    of lookups in the location table, though it is a bit over the top.
    """

    TYPES = Choices(
        (0, "continent", _("continent")),
        (1, "country", _("country")),
        (2, "region", _("region")),
    )

    name = models.CharField(
        max_length=255, blank=False, null=False,
        help_text="Name of the country or region",
    )

    iso_code = models.CharField(
        max_length=3, blank=False, null=False,
        help_text="ISO code for the region or country",
    )

    region_type = models.PositiveSmallIntegerField(
        choices=TYPES, default=TYPES.country,
        help_text="Type of geographic region"
    )

    parent = models.ForeignKey(
        "diary.GeoEntity", models.SET_NULL, related_name="+", null=True, blank=True, default=None,
        help_text="The geographic entity that contains the current entity",
    )

    class Meta:
        db_table = "geo_entities"
        verbose_name = "geographic entity"
        verbose_name_plural = "geographic entities"
        unique_together = ("name", "iso_code", "region_type")

    def __str__(self):
        return self.name


class Tabs(TimeStampedModel):
    """
    A sidecar object that counts the number of tabs open during the dairy entry.
    """

    memo = models.OneToOneField(
        "diary.Memo", models.CASCADE,
        null=False, blank=False, related_name="tabs",
        help_text="The memo associated with the tabs count",
    )

    desktop_windows = models.PositiveSmallIntegerField(
        default=None, null=True, blank=True,
        help_text="The number of desktop windows open"
    )

    desktop_tabs = models.PositiveSmallIntegerField(
        default=None, null=True, blank=True,
        help_text="The total number of desktop tabs open in all windows"
    )

    mobile_tabs = models.PositiveSmallIntegerField(
        default=None, null=True, blank=True,
        help_text="The number of tabs open on your mobile device"
    )

    tablet_tabs = models.PositiveSmallIntegerField(
        default=None, null=True, blank=True,
        help_text="The number of tabs open on your tablet device"
    )

    class Meta:
        db_table = "browser_tabs"
        verbose_name = "Browser Tab Count"
        verbose_name_plural = "Browser Tab Counts"
        ordering = ("-memo__date",)
        get_latest_by = "memo__date"
