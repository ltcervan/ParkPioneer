import requests
from django.conf import settings
from django.http import JsonResponse

def search_parks(request):
    # Extract search parameters from the request
    park_name = request.GET.get('parkName')
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')

    # Construct the API URL with query parameters
    api_url = f"https://developer.nps.gov/api/v1/parks?parkCode={park_name}&api_key={settings.NPS_API_KEY}"

    response = requests.get(api_url)
    data = response.json()

    # Optionally filter events by date here if the NPS API does not support date filtering

    return JsonResponse(data)
