# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# BITE - A Basic/IoT/Example
# Copyright (C) 2020-2021 Daniele Viganò <daniele@vigano.me>
#
# BITE is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BITE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""bite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.contrib import admin
from django.conf import settings
from django.urls import include, path

from dps import urls as dps_urls
from telemetry import urls as telemetry_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ht/', include('health_check.urls')),
    path('dps/', include(dps_urls)),
    path('telemetry/', include(telemetry_urls)),
]

if settings.DEBUG:
    from django.views.generic import TemplateView
    from rest_framework.schemas import get_schema_view

    urlpatterns += [
        path('swagger/', TemplateView.as_view(
            template_name='swagger.html',
            extra_context={'schema_url': 'openapi-schema'}
        ), name='swagger'),
        path('openapi', get_schema_view(
            title="BITE - A Basic/IoT/Example",
            description="BITE API for IoT",
            version="1.0.0"
        ), name='openapi-schema'),
    ]
