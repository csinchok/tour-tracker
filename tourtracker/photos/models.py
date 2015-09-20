import os
import exifread

from datetime import datetime
from django.core.files import File
from django.db import models
from django.utils import timezone

from tourtracker.rides.models import Ride
from tourtracker.utils.timezonedb import get_timezone


def convert_gps_ratio(values):
    deg, mins, secs = [x.num / float(x.den) for x in values]
    return deg + (mins / 60) + (secs / 3600)


class PhotoManager(models.Manager):

    def create_from_file(self, file_path):

        photo = Photo()

        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
            if 'GPS GPSLongitude' in tags:
                # We have gps...
                lon = convert_gps_ratio(tags['GPS GPSLongitude'].values)
                if tags['GPS GPSLongitudeRef'].values == 'W':
                    lon *= -1

                lat = convert_gps_ratio(tags['GPS GPSLatitude'].values)
                if tags['GPS GPSLatitudeRef'].values == 'S':
                    lat *= -1

                photo.latitude = lat
                photo.longitude = lon

            if 'Image DateTime' in tags:
                # We have a date...
                date_string = tags['Image DateTime'].values

                date_fmt = '%Y:%m:%d %H:%M:%S'
                timestamp_naiive = datetime.strptime(date_string, date_fmt)

                tz = timezone.get_default_timezone()
                if photo.latitude and photo.longitude:
                    tz = get_timezone(photo.latitude, photo.longitude)

                photo.timestamp = timestamp_naiive.replace(tzinfo=tz)

                # Now let's see if there's a matching ride!
                rides = Ride.objects.filter(
                    start__lte=photo.timestamp,
                    end__gte=photo.timestamp
                )
                if rides.count() == 1:
                    photo.ride = rides[0]

            photo.save()
            photo.src.save(os.path.basename(file_path), File(f))

            return photo


def photo_upload_to(instance, filename):
    return 'photos/{}/{}'.format(instance.pk, filename)


class Photo(models.Model):

    src = models.ImageField(upload_to=photo_upload_to)
    caption = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField()

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    ride = models.ForeignKey(Ride, null=True, blank=True, related_name='photos')

    objects = PhotoManager()

    @property
    def thumbnail_url(self):
        return '/photos/thumbnail/{}.jpg'.format(self.pk)
