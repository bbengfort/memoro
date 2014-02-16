# memorandi.authors.mixins
# Class mixins as authentication helpers
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Feb 15 21:35:13 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: mixins.py [] benjamin@bengfort.com $

"""
Class mixins as authentication helpers
"""

##########################################################################
## Imports
##########################################################################

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt, csrf_protect

##########################################################################
## Mixins
##########################################################################

class DispatchProtectionMixin(object):
    """
    Protect the dispatch method with CSRF and no Caching
    """

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(DispatchProtectionMixin, self).dispatch(*args, **kwargs)

class LoginRequiredMixin(object):
    """
    This view requires an authenticated user
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class CsrfExemptMixin(object):
    """
    FormViews that add this mixin do not check CSRF tags
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(*args, **kwargs)
