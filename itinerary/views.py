from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Itinerary, Event
from django.contrib import messages
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
def search_park_events(request, itinerary_id):
    park_title = request.session.get('park_title')
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    
    api_url = "https://developer.nps.gov/api/v1/events"
    params = {
        'q': park_title,
        'startDate': start_date,
        'endDate': end_date,
        'api_key': settings.NPS_API_KEY,
    }
    
    response = requests.get(api_url, params=params)
    events = []
    if response.status_code == 200:
        events = response.json().get('data', [])
    return render(request, 'itinerary/event_list.html', {'events': events, 'itinerary_id': itinerary_id})

@require_POST
def add_event_to_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_id, user=request.user)
    # Create a new Event instance with data from the form
    new_event = Event(
        itinerary=itinerary,
        title=request.POST.get('title'),
        time=request.POST.get('time'),
        date=request.POST.get('date'),
        location=request.POST.get('location'),
    )
    new_event.save()
    messages.success(request, 'Event added to your itinerary!')
    return redirect('itinerary_detail', itinerary_id=itinerary.id)


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

@login_required
@login_required
def event_details(request, event_id):
    # Make a request to the NPS API to fetch event details based on the event_id
    api_url = f"https://developer.nps.gov/api/v1/events/{event_id}"
    params = {
        'api_key': settings.NPS_API_KEY,
    }
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        event_data = response.json().get('data', {})
        if event_data:
            # Create or update the Event object based on the retrieved data
            event, created = Event.objects.update_or_create(
                id=event_data.get('id'),
                defaults={
                    'title': event_data.get('title'),
                    'start_date': event_data.get('startDate'),
                    'end_date': event_data.get('endDate'),
                    'description': event_data.get('description'),
                    # Add other fields as necessary
                }
            )
            return render(request, 'itinerary/event_details.html', {'event': event})
        else:
            return render(request, 'itinerary/event_details.html', {'error': 'Event not found'})
    else:
        return render(request, 'itinerary/event_details.html', {'error': 'Failed to fetch event details from the API'})

