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

import json
from django.test import TestCase, Client
from dps.models import Device, WhiteList


class ApiTestCase(TestCase):
    c = Client()

    payload = {
        "id": "sensor.server.domain",
        "light": 434,
        "temperature": {
            "celsius": 27.02149,
            "raw": 239,
            "volts": 0.770215
        }
    }

    telemetry = {
        'device': 'test1234',
        'clock': 1591194712,
        'payload': json.dumps(payload)
    }

    def setUp(self):
        WhiteList.objects.create(serial='test1234')
        Device.objects.create(serial='test1234')

    def test_no_device(self):
        fake_telemetry = dict(self.telemetry)  # make a copy of the dict
        fake_telemetry['device'] = '1234test'
        response = self.c.post('/telemetry/', fake_telemetry)
        self.assertEqual(response.status_code, 400)

    def test_empty_telemetry(self):
        fake_telemetry = dict(self.telemetry)  # make a copy of the dict
        fake_telemetry['payload'] = ''
        response = self.c.post('/telemetry/', fake_telemetry)
        self.assertEqual(response.status_code, 400)

    def test_telemetry_post(self):
        response = self.c.post('/telemetry/', self.telemetry)
        self.assertEqual(response.status_code, 201)

    def test_telemetry_get(self):
        response = self.c.post('/telemetry/', self.telemetry)
        response = self.c.get('/telemetry/test1234/last/')
        self.assertEqual(
            response.json()['device'], 'test1234')
        self.assertEqual(
            response.json()['transport'], 'http')
        self.assertJSONEqual(
            json.dumps(response.json()['payload']),
            json.dumps(self.payload))
