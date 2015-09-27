from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import Ride


def listing(request):
    rides = Ride.objects.all()
    return render(request, 'listing.html', {'rides': rides})


def detail(request, pk):
    ride = get_object_or_404(Ride, pk=pk)
    return render(request, 'detail.html', {'ride': ride})


def ride_data(request, pk):

    ride = get_object_or_404(Ride, pk=pk)
    return JsonResponse({
        'average_speed': ride.average_speed,
        'distance': ride.distance,
        'data': ride.data
    })
