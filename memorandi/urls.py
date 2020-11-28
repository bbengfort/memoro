# memorandi
# memorandi URL Configuration
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Nov 28 13:44:01 2020 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
memorandi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from django.urls import path


##########################################################################
## URL Patterns
##########################################################################

urlpatterns = [
    path('admin/', admin.site.urls),
]
