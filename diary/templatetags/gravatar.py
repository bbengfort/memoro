# diary.templatetags.gravatar
# Gravatar helpers for faculty profile images
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Dec 02 12:48:26 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: gravatar.py [] benjamin@bengfort.com $

"""
Gravatar helpers for faculty profile images
"""

##########################################################################
## Imports
##########################################################################

from hashlib import md5
from django import template

register = template.Library()


##########################################################################
## Template Tags
##########################################################################

@register.filter(name='gravatar')
def gravatar(user, size=35):
    if hasattr(user, "faculty") and user.faculty is not None:
        email = user.faculty.get_email()
    else:
        email = user.email

    email = str(user.email.strip().lower()).encode('utf-8')
    email_hash = md5(email).hexdigest()
    url = "//www.gravatar.com/avatar/{0}?s={1}&d=identicon&r=PG"
    return url.format(email_hash, size)
