import csv
import json
import os
import pytz
from datetime import datetime, timedelta

from django.core.files import File
from django.db import models

from tourtracker.utils.timezonedb import get_timezone


class RideManager(models.Manager):

    def create_from_cyclemeter(self, file_path):

        coordinates = []
        ride = Ride(name='Ride')

        map_bounds = {
            'lat_min': 0,
            'lat_max': 0,

            'lon_min': 0,
            'lon_max': 0
        }

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

                    map_bounds = {
                        'lat_min': this_coord[1],
                        'lat_max': this_coord[1],

                        'lon_min': this_coord[0],
                        'lon_max': this_coord[0]
                    }
                else:

                    map_bounds = {
                        'lat_min': min(this_coord[1], map_bounds['lat_min']),
                        'lat_max': max(this_coord[1], map_bounds['lat_max']),

                        'lon_min': min(this_coord[0], map_bounds['lon_min']),
                        'lon_max': max(this_coord[0], map_bounds['lon_max'])
                    }

            else:
                """Let's save the "ratio" of the map. We'll use this to figure
                out which template to use...
                """
                width = map_bounds['lon_max'] - map_bounds['lon_min']
                height = map_bounds['lat_max'] - map_bounds['lat_min']
                ride.map_ratio = width / float(height)

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

            ride.ride_file.save(os.path.basename(file_path), File(csvfile))

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

    map_ratio = models.FloatField()

    ride_file = models.FileField(upload_to='ride_files')

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
