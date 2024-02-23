from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Itinerary, Event
from .forms import ItineraryForm
from django.conf import settings
from datetime import timedelta
import requests

def itinerary_list(request):
    itineraries = Itinerary.objects.filter(user=request.user)
    return render(request, 'itinerary/itinerary_list.html', {'itineraries': itineraries})

def main_view(request):
    return render(request, 'itinerary/main.html')


## ============= Authentication Required =======================
@login_required
def create_itinerary(request):
    if request.method == 'POST':
        form = ItineraryForm(request.POST)
        if form.is_valid():
            itinerary = form.save(commit=False)
            itinerary.user = request.user
            itinerary.save()
            return redirect('itinerary_list')
    else:
        form = ItineraryForm()
    return render(request, 'itinerary/create_itinerary.html', {'form': form})


@login_required
def itinerary_list(request):
    itineraries = Itinerary.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'itinerary/itinerary_list.html', {'itineraries': itineraries})
    
@login_required
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


@login_required
def itinerary_detail(request, itinerary_id):
    itinerary = Itinerary.objects.get(pk=itinerary_id)
    start_date = itinerary.start_date
    end_date = itinerary.end_date
    number_of_days = (end_date - start_date).days + 1  # +1 to include both start and end dates

    # Gather events by date
    days_events = {}
    for i in range(number_of_days):
        day = start_date + timedelta(days=i)
        events_on_day = itinerary.events.filter(date=day)
        days_events[day] = events_on_day

    context = {
        'itinerary': itinerary,
        'days_events': days_events.items(),
    }
    return render(request, 'itinerary/itinerary_detail.html', context)
