import datetime
import json
import os
import pytz
import shutil
from httmock import all_requests, HTTMock

from django.conf import settings
from django.test import TestCase

from tourtracker.rides.models import Ride


@all_requests
def timezonedb_response(url, request):
    # Mocking out the timezonedb response, so I don't call it in the tests
    content = json.dumps({
        'abbreviation': 'CDT',
        'countryCode': 'US',
        'message': '',
        'status': 'OK',
        'timestamp': 1442512892,
        'dst': '1',
        'zoneName': 'America/Chicago',
        'gmtOffset': '-18000'
    }).encode('utf-8')
    return {
        'status_code': 200,
        'content': content,
        'headers': {'Content-Type': 'application/json'}
    }


class RideTest(TestCase):

    def setUp(self):
        # Kill any existing media files...
        rides_root = os.path.join(settings.MEDIA_ROOT, 'ride_files')
        for item in os.listdir(rides_root):
            if not item.endswith('README.md'):
                os.remove(os.path.join(rides_root, item))

    def tearDown(self):
        # Kill any remaining media files...
        rides_root = os.path.join(settings.MEDIA_ROOT, 'ride_files')
        for item in os.listdir(rides_root):
            if not item.endswith('README.md'):
                os.remove(os.path.join(rides_root, item))

    def test_csv_ingestion(self):

        file_path = os.path.join(os.path.dirname(__file__), 'test_ride.csv')

        with HTTMock(timezonedb_response):
            ride = Ride.objects.create_from_cyclemeter(file_path)

        expected_start = datetime.datetime(
            year=2015, month=9, day=17, hour=12, minute=52, second=21,
            tzinfo=pytz.timezone('America/Chicago'))
        self.assertEqual(ride.start, expected_start)

        self.assertEqual(len(ride.path['geometry']['coordinates']), 3240)
        self.assertEqual(ride.average_speed, 14.65)
        self.assertEqual(ride.distance, 20.63)
