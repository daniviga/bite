import json
from django.test import TestCase, Client
from api.models import Device, WhiteList


class ApiTestCase(TestCase):
    c = Client()

    payload = {
        'id': 'sensor.server.domain',
        'light': 434,
        'temperature': {
            'celsius': 27.02149,
            'raw': 239,
            'volts': 0.770215
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
            json.dumps(response.json()['payload']), self.payload)
