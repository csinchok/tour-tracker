from django.core.management.base import BaseCommand
from tourtracker.rides.models import Ride
from tourtracker.photos.models import Photo


class Command(BaseCommand):
    help = 'Imports sample data'

    def handle(self, *args, **options):
        ride = Ride.objects.create_from_cyclemeter('./tourtracker/rides/tests/test_ride.csv')

        Photo.objects.create_from_file('./tourtracker/photos/tests/IMG_4430.JPG')
        Photo.objects.create_from_file('./tourtracker/photos/tests/IMG_4431.JPG')

        for photo in Photo.objects.all():
            photo.ride = ride
            photo.save()
