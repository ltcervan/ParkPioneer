from django.http import JsonResponse
from django.conf import settings
from .models import Itinerary
from django import forms
import requests

def search_parks(request):
    park_title = request.GET.get('parkName')
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')
    api_url = f"https://developer.nps.gov/api/v1/parks?parkCode={park_title}&api_key={settings.NPS_API_KEY}"

    response = requests.get(api_url)
    data = response.json()

    return JsonResponse(data)

class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['title', 'park_title', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

