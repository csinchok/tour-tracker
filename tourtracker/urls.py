from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'tourtracker.rides.views.listing'),
    url(r'^rides/', include('tourtracker.rides.urls')),
    url(r'^photos/', include('tourtracker.photos.urls')),
]
