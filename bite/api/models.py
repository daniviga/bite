# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# BITE - A Basic/IoT/Example
# Copyright (C) 2020 Daniele Viganò <daniele@vigano.me>
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

import uuid

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


def device_validation(value):
    if settings.SKIP_WHITELIST and settings.DEBUG:
        return  # skip validation in debug mode when SKIP_WHITELIST is True

    published_devices = WhiteList.objects.filter(
        serial=value,
        is_published=True
    )
    if not published_devices:
        raise ValidationError("Device is not published")


class WhiteList(models.Model):
    serial = models.CharField(primary_key=True, max_length=128)
    creation_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['serial', 'updated_time']

    def __str__(self):
        return self.serial


class Device(models.Model):
    serial = models.CharField(max_length=128, unique=True,
                              validators=[device_validation])
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_time', 'serial']

    def __str__(self):
        return self.serial
