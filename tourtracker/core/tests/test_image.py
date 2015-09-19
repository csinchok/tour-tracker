import datetime
import json
import os
import pytz
import shutil

from httmock import all_requests, HTTMock

from django.conf import settings
from django.test import TestCase

from tourtracker.core.models import Photo, Ride


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


class ImageTest(TestCase):

    def setUp(self):
        # Kill any existing media files...
        photo_root = os.path.join(settings.MEDIA_ROOT, 'photos')
        for item in os.listdir(photo_root):
            if not item.endswith('README.md'):
                shutil.rmtree(os.path.join(photo_root, item))

    def tearDown(self):
        # Kill any remaining media files...
        photo_root = os.path.join(settings.MEDIA_ROOT, 'photos')
        for item in os.listdir(photo_root):
            if not item.endswith('README.md'):
                shutil.rmtree(os.path.join(photo_root, item))

    def test_image_ingestion(self):
        # Let's create a ride that this will match...
        ride_kwargs = {
            'start': datetime.datetime(
                year=2015, month=9, day=17, hour=12, minute=52, second=21,
                tzinfo=pytz.timezone('America/Chicago')),
            'end': datetime.datetime(
                year=2015, month=9, day=17, hour=15, minute=52, second=21,
                tzinfo=pytz.timezone('America/Chicago')),
            'distance': 1.0,
            'average_speed': 1.0,
            'ride_time': datetime.timedelta(hours=5),
            'stopped_time': datetime.timedelta(hours=1)
        }

        test_ride = Ride.objects.create(**ride_kwargs)

        file_path = os.path.join(os.path.dirname(__file__), 'IMG_4430.JPG')

        with HTTMock(timezonedb_response):
            photo = Photo.objects.create_from_file(file_path)

        self.assertTrue(photo.src.path.endswith('photos/1/IMG_4430.JPG'))
        self.assertEqual(photo.ride, test_ride)
