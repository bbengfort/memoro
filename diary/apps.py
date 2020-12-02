# diary.apps
# App specific configuration for lazy loading.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Dec 02 13:14:57 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: apps.py [] benjamin@bengfort.com $

"""
App specific configuration for lazy loading.
"""

##########################################################################
## Imports
##########################################################################

from django.apps import AppConfig

##########################################################################
## Configure App Here
##########################################################################

class DiaryConfig(AppConfig):
    name = 'diary'
