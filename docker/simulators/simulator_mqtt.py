#!/usr/bin/env python3

import os
import json
import string
import random
import datetime
import urllib3
from time import sleep
import paho.mqtt.publish as publish

DEBUG = bool(os.environ.get('IOT_DEBUG', False))
http = urllib3.PoolManager()


def post_json(host, url, data):
    json_data = json.dumps(data)

    if DEBUG:
        print(json_data)

    encoded_data = json_data.encode('utf8')

    while True:
        try:
            r = http.request(
                'POST',
                host + url,
                body=encoded_data,
                headers={'content-type': 'application/json'})
            return r
        except urllib3.exceptions.MaxRetryError:
            pass

        sleep(10)  # retry in 10 seconds


def publish_json(host, data):
    json_data = json.dumps(data)
    serial = data['device']

    if DEBUG:
        print(json_data)

    encoded_data = json_data.encode('utf8')

    publish.single(
        topic=serial,
        payload=encoded_data,
        hostname=host.split(':')[0],
        port=int(host.split(':')[1]),
        client_id=serial,
        # auth=auth FIXME
    )


def main():
    host = os.environ.get('IOT_HOST', 'http://127.0.0.1:8000')
    mqtt_host = os.environ.get('IOT_MQTT_HOST', '127.0.0.1:1883')
    subscribe = '/api/device/subscribe/'
    delay = int(os.environ.get('IOT_DELAY', 10))
    serial = os.environ.get('IOT_SERIAL')

    if serial is None:
        serial = ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=8))

    data = {'serial': serial}
    post_json(host, subscribe, data)

    data = {
        'device': serial,
        'clock': int(datetime.datetime.now().timestamp()),
    }

    while True:
        payload = {
            'id': 'device_mqtt_simulator',
            'light': random.randint(300, 500),
            'temperature': {
                'celsius': round(random.uniform(20, 28), 1)}
        }
        publish_json(mqtt_host, {**data, 'payload': payload})
        sleep(delay)


if __name__ == "__main__":
    main()
