import csv
import exifread
import json
import requests
import pytz

from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.utils import timezone


def get_timezone(lat, lng):
    """Returns a timezone for the given lat, lon pair"""

    response = requests.get('http://api.timezonedb.com/', params={
        'format': 'json',
        'key': settings.TIMEZONE_DB_KEY,
        'lat': lat,
        'lng': lng
    })
    zone_name = response.json()['zoneName']
    return pytz.timezone(zone_name)


class RideManager(models.Manager):

    def create_from_cyclemeter(self, file_path):

        coordinates = []
        ride = Ride(name='Ride')

        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            tz = pytz.utc

            for index, row in enumerate(reader):
                this_coord = [float(row['Longitude']), float(row['Latitude'])]

                coordinates.append(this_coord)

                date_fmt = '%Y-%m-%d %H:%M:%S'

                if index == 0:
                    tz = get_timezone(*this_coord)

                    # Now we record the ride start time
                    ride.start = datetime.strptime(row['Time'], date_fmt).replace(tzinfo=tz)
            else:
                # Here, 'row' is the last row in the file...
                ride.end = datetime.strptime(row['Time'], date_fmt).replace(tzinfo=tz)
                ride.distance = float(row['Distance (miles)'])
                ride.average_speed = float(row['Average Speed (mph)'])

                ride_time = list(map(int, row['Ride Time'].split(':')))
                ride.ride_time = timedelta(
                    hours=ride_time[0],
                    minutes=ride_time[1],
                    seconds=ride_time[2])

                stopped_time = list(map(int, row['Stopped Time'].split(':')))
                ride.stopped_time = timedelta(
                    hours=stopped_time[0],
                    minutes=stopped_time[1],
                    seconds=stopped_time[2])

        path_feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': coordinates
            }
        }
        ride.path = path_feature

        ride.save()
        return ride


class Ride(models.Model):

    name = models.CharField(max_length=255)
    _path = models.TextField()

    start = models.DateTimeField()
    end = models.DateTimeField()

    distance = models.FloatField()
    average_speed = models.FloatField()

    ride_time = models.DurationField()
    stopped_time = models.DurationField()

    objects = RideManager()

    @property
    def path(self):
        data = json.loads(self._path)
        data['properties'] = {}
        return data

    @path.setter
    def path(self, data):
        self._path = json.dumps(data)


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
            return photo


class Photo(models.Model):

    src = models.ImageField()
    caption = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField()

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    ride = models.ForeignKey(Ride, null=True, blank=True)

    objects = PhotoManager()
