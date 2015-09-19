from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def mapbox_access_token():
    return settings.MAPBOX_ACCESS_TOKEN
