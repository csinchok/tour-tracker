from django.conf.urls import url

urlpatterns = [
    url(r'^thumbnail/(?P<pk>\d+)\.jpg$', 'tourtracker.photos.views.thumbnail')
]
