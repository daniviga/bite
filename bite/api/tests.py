from django.test import TestCase, Client
from api.models import Device, WhiteList


class ApiTestCase(TestCase):
    c = Client()

    def setUp(self):
        WhiteList.objects.create(serial='test1234')
        Device.objects.create(serial='test1234')

    def test_no_whitelist(self):
        response = self.c.post('/api/device/subscribe/',
                               {'serial': 'test12345'})
        self.assertEqual(response.status_code, 400)

    def test_subscribe_post(self):
        WhiteList.objects.create(serial='test12345')
        response = self.c.post('/api/device/subscribe/',
                               {'serial': 'test12345'})
        self.assertEqual(response.status_code, 201)

    def test_subscribe_get(self):
        response = self.c.get('/api/device/list/')
        self.assertEqual(
            response.json()[0]['serial'], 'test1234')
