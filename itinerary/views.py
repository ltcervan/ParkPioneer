from django.shortcuts import render, redirect
from .models import Itinerary
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests

def itinerary_list(request):
    itineraries = Itinerary.objects.filter(user=request.user)
    return render(request, 'itinerary/itinerary_list.html', {'itineraries': itineraries})

def main_view(request):
    return render(request, 'itinerary/main.html')


@login_required
def create_itinerary(request):
    if request.method == 'POST':
        # Process the form data, create an Itinerary, and redirect
        # ...
        return redirect('some_view_name')
    else:
        # If not POST, render the form page
        return render(request, 'itinerary/create_itinerary.html')
    

def search_park_events(request):
    context = {}
    if 'park_name' in request.GET:
        park_name = request.GET.get('park_name')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Construct the API URL with your parameters
        api_url = f"https://developer.nps.gov/api/v1/events"
        params = {
            'q': park_name,
            'startDate': start_date,
            'endDate': end_date,
            'api_key': settings.NPS_API_KEY,
        }
        
        # Make the API request
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            # Parse the response data
            context['events'] = response.json()['data']
        else:
            context['error'] = "An error occurred while trying to retrieve events."
    
    return render(request, 'itinerary/search_park_events.html', context)

