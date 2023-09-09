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

from django.test import TestCase, Client
from dps.models import Device, WhiteList


class DPSTestCase(TestCase):
    c = Client()

    def setUp(self):
        WhiteList.objects.create(serial='test1234')
        Device.objects.create(serial='test1234')

    def test_no_whitelist(self):
        response = self.c.post('/dps/device/provision/',
                               {'serial': 'test12345'})
        self.assertEqual(response.status_code, 400)

    def test_provision_post(self):
        WhiteList.objects.create(serial='test12345')
        response = self.c.post('/dps/device/provision/',
                               {'serial': 'test12345'})
        self.assertEqual(response.status_code, 201)

    def test_provision_get(self):
        response = self.c.get('/dps/device/list/')
        self.assertEqual(
            response.json()[0]['serial'], 'test1234')
