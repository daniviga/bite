#!/usr/bin/env python3

import os
import json
import string
import random
import datetime
import urllib3
import argparse

from time import sleep
import paho.mqtt.publish as publish

DEBUG = bool(os.environ.get('IOT_DEBUG', False))
http = urllib3.PoolManager()


def post_json(endpoint, url, data):
    json_data = json.dumps(data)

    if DEBUG:
        print(json_data)

    encoded_data = json_data.encode('utf8')

    while True:
        try:
            r = http.request(
                'POST',
                endpoint + url,
                body=encoded_data,
                headers={'content-type': 'application/json'})
            return r
        except urllib3.exceptions.MaxRetryError:
            pass

        sleep(10)  # retry in 10 seconds


def publish_json(transport, endpoint, data):
    json_data = json.dumps(data)
    serial = data['device']

    if DEBUG:
        print(json_data)

    encoded_data = json_data.encode('utf8')

    publish.single(
        topic=serial,
        payload=encoded_data,
        hostname=endpoint.split(':')[0],
        port=int(endpoint.split(':')[1]),
        client_id=serial,
        transport=('websockets' if transport == 'ws' else 'tcp'),
        # auth=auth FIXME
    )


def main():
    parser = argparse.ArgumentParser(
        description='IoT simulator oprions')

    parser.add_argument('-e', '--endpoint',
                        default=os.environ.get('IOT_HTTP',
                                               'http://127.0.0.1:8000'),
                        help='IoT HTTP endpoint')
    parser.add_argument('-m', '--mqtt',
                        default=os.environ.get('IOT_MQTT',
                                               '127.0.0.1:1883'),
                        help='IoT MQTT endpoint')
    parser.add_argument('-t', '--transport',
                        choices=['mqtt', 'ws', 'http'],
                        default=os.environ.get('IOT_TL', 'http'),
                        help='IoT transport layer')
    parser.add_argument('-s', '--serial',
                        default=os.environ.get('IOT_SERIAL'),
                        help='IoT device serial number')
    parser.add_argument('-d', '--delay', metavar='s', type=int,
                        default=os.environ.get('IOT_DELAY', 10),
                        help='Delay between requests')
    args = parser.parse_args()

    subscribe = '/api/device/subscribe/'
    telemetry = '/telemetry/'

    if args.serial is None:
        args.serial = ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=8))

    data = {'serial': args.serial}
    post_json(args.endpoint, subscribe, data)

    while True:
        data = {
            'device': args.serial,
            'clock': int(datetime.datetime.now().timestamp()),
        }
        payload = {
            'id': 'device_simulator',
            'light': random.randint(300, 500),
            'temperature': {
                'celsius': round(random.uniform(20, 28), 1)}
        }
        if args.transport == 'http':
            post_json(args.endpoint, telemetry, {**data, 'payload': payload})
        elif args.transport in ('mqtt', 'ws'):
            publish_json(
                args.transport, args.mqtt, {**data, 'payload': payload})
        else:
            raise NotImplementedError
        sleep(args.delay)


if __name__ == "__main__":
    main()
