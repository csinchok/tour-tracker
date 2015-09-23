import os

from django.core.management.base import BaseCommand
from tourtracker.rides.models import Ride
from tourtracker.photos.models import Photo


class Command(BaseCommand):
    help = 'Imports sample data'

    def handle(self, *args, **options):
        ride = Ride.objects.create_from_cyclemeter('./tourtracker/rides/tests/test_rides/wi_ride.csv')

        test_photo_dir = './tourtracker/photos/tests/test_photos'

        for filename in os.listdir('./tourtracker/photos/tests/test_photos'):
            Photo.objects.create_from_file(os.path.join(test_photo_dir, filename))

        # for photo in Photo.objects.all():
        #     photo.ride = ride
        #     photo.save()
