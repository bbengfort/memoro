#!/usr/bin/env python
# manage
# Django's command-line utility for administrative tasks.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Nov 28 13:41:44 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: manage.py [] benjamin@bengfort.com $

"""
Django's command-line utility for administrative tasks.
"""

##########################################################################
## Imports
##########################################################################

import os
import sys

from dotenv import find_dotenv, load_dotenv


##########################################################################
## Load environment
##########################################################################

load_dotenv(find_dotenv())


##########################################################################
## Main Methods
##########################################################################

def main():
    """
    Run administrative tasks.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memoro.settings.development')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
