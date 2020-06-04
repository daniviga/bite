#!/usr/bin/env python3

import os
import json
import string
import random
import datetime
import urllib3
from time import sleep

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


def main():
    host = os.environ.get('IOT_HOST', 'http://127.0.0.1:8000')
    subscribe = '/api/subscribe/'
    telemetry = '/telemetry/'
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
        'payload': {
            'id': 'device_http_simulator',
            'light': random.randint(300, 500),
            "temperature": {
                "celsius": random.uniform(20, 28)
            }
        }
    }

    while True:
        post_json(host, telemetry, data)
        sleep(delay)


if __name__ == "__main__":
    main()
