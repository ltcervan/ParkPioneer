from django.shortcuts import render
from .models import Itinerary

def itinerary_list(request):
    itineraries = Itinerary.objects.filter(user=request.user)
    return render(request, 'itinerary/itinerary_list.html', {'itineraries': itineraries})

