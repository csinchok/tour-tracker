from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'tourtracker.core.views.listing'),
    url(r'^rides/(?P<pk>\d+)\.json$', 'tourtracker.core.views.geojson')
]
