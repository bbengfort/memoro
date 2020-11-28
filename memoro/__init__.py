# memoro
# Project environment for the memoro web application.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Nov 28 13:44:01 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Project environment for the memoro web application.
"""

##########################################################################
## Imports
##########################################################################

from .version import __version_info__, get_version


##########################################################################
## Package Info
##########################################################################

__version__ = get_version()
