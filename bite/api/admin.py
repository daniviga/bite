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

from django.contrib import admin
from api.models import Device, WhiteList


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_time', 'updated_time',)
    list_filter = ('serial',)
    search_fields = ('serial',)

    fieldsets = (
        (None, {
            'fields': ('serial', )
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': ('creation_time', 'updated_time',)
        }),
    )


@admin.register(WhiteList)
class WhiteListAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_time', 'updated_time',)
    list_filter = ('serial',)
    search_fields = ('serial',)

    fieldsets = (
        (None, {
            'fields': ('serial', 'is_published',)
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': ('creation_time', 'updated_time',)
        }),
    )
