from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'tourtracker.rides.views.listing'),
    url(r'^rides/(?P<pk>\d+)\.json$', 'tourtracker.rides.views.geojson')
]
