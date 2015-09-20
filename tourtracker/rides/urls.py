from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<pk>\d+)\.json$', 'tourtracker.rides.views.geojson')
]
