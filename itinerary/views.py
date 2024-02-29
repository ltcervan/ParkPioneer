from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from datetime import timedelta, datetime
from .models import Itinerary, Event
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .forms import ItineraryForm
from django.conf import settings
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
def update_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_id, user=request.user)
    if request.method == 'POST':
        form = ItineraryForm(request.POST, instance=itinerary)
        if form.is_valid():
            form.save()
            return redirect('itinerary_list')
    else:
        form = ItineraryForm(instance=itinerary)
    return render(request, 'itinerary/update_itinerary.html', {'form': form})

@login_required
def delete_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_id, user=request.user)
    if request.method == 'POST':
        itinerary.delete()
        return redirect('itinerary_list')
    return render(request, 'itinerary/delete_itinerary.html', {'itinerary': itinerary})

@login_required
def itinerary_list(request):
    itineraries = Itinerary.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'itinerary/itinerary_list.html', {'itineraries': itineraries})
@login_required
def delete_itinerary(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk)
    if request.method == 'POST':
        itinerary.delete()
        return redirect('itinerary_list')
    return render(request, 'itinerary/delete_itinerary.html', {'itinerary': itinerary})
    
@login_required
def search_park_events(request, itinerary_id):
    event_id = request.GET.get('event_id')
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
    print(response)
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
    print('============ new event==============', new_event)
    new_event.save()
    messages.success(request, 'Event added to your itinerary!')
    return redirect('itinerary_detail', itinerary_id=itinerary.id)


@login_required
def itinerary_detail(request, itinerary_id):
    itinerary = Itinerary.objects.get(pk=itinerary_id)
    start_date = itinerary.start_date
    end_date = itinerary.end_date
    number_of_days = (end_date - start_date).days + 1  

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
def event_details(request, event_id):
    # Make a request to the NPS API to fetch event details based on the event_id
    api_url = f"https://developer.nps.gov/api/v1/events"
    params = {
        'api_key': settings.NPS_API_KEY,
        'id': event_id
    }
    response = requests.get(api_url, params=params)
    print(response)

    if response.status_code == 200:
        event_data = response.json().get('data', [])
        print(event_data, "event_data")
        for event in event_data:
            print(event, "event")
            # data = event.json()
        #     return JsonResponse(event)
        # else:
        #     return JsonResponse({'error': 'Event not found'}, status = 404)

            # Create or update the Event object based on the retrieved data
            # event, created = Event.objects.update_or_create(
            #     id=event_data.get('id'),
            #     defaults={
            #         'title': event_data.get('title'),
            #         'start_date': event_data.get('startDate'),
            #         'end_date': event_data.get('endDate'),
            #         'description': event_data.get('description'),
            #         # Add other fields as necessary
            #     }
            # )
            return render(request, 'itinerary/event_details.html', {'event': event})
        else:
            return render(request, 'itinerary/event_details.html', {'error': 'Event not found'})
    # else:
        # return render(request, 'itinerary/event_details.html', {'error': 'Failed to fetch event details from the API'})

    
@login_required
def add_event_to_itinerary(request, itinerary_id, event_id, event_date):
    print("Event ID:", event_id)
    print("Event Date:", event_date)
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


# def add_event_to_itinerary(request, itinerary_id, event_date):
#     itinerary = get_object_or_404(Itinerary, pk=itinerary_id, user=request.user)
#     event_id = request.POST.get('eventId')
#     event = get_object_or_404(Event, pk=event_id)
#     # Convert event_date string to datetime object
#     event_date = datetime.strptime(event_date, '%Y-%m-%d').date()
#     # Set event date and save
#     event.date = event_date
#     event.save()
#     itinerary.events.add(event)
#     messages.success(request, 'Event added to your itinerary!')
#     return redirect('itinerary/itinerary_detail', itinerary_id=itinerary.id)

