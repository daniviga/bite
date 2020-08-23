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

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from api.models import Device


def telemetry_validation(value):
    if not value:
        raise ValidationError("No telemetry has been sent")


class Telemetry(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    time = models.DateTimeField(primary_key=True, auto_now_add=True)
    transport = models.CharField(max_length=4,
                                 choices=[('http', 'http'), ('mqtt', 'mqtt')],
                                 default='http')
    clock = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=True)
    payload = models.JSONField(validators=[telemetry_validation])

    class Meta:
        ordering = ['-time', 'device']
        verbose_name_plural = "Telemetry"

    def __str__(self):
        return str(self.time)
