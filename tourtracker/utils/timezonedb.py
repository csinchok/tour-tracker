import pytz
import requests

from django.conf import settings


def get_timezone(lat, lng):
    """Returns a timezone for the given lat, lon pair"""

    response = requests.get('http://api.timezonedb.com/', params={
        'format': 'json',
        'key': settings.TIMEZONE_DB_KEY,
        'lat': lat,
        'lng': lng
    })

    zone_name = response.json()['zoneName']
    if zone_name == '':
        print(response.json())
    return pytz.timezone(zone_name)
