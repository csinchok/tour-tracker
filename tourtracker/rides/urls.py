from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<pk>\d+)$', 'tourtracker.rides.views.detail'),
    url(r'^(?P<pk>\d+)\.json$', 'tourtracker.rides.views.ride_data')
]
