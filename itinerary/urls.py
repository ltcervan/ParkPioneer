from django.urls import path
from . import views
from .views import main_view,itinerary_list, create_itinerary, search_park_events, itinerary_detail, add_event_to_itinerary, event_details  # Replace with your actual view that renders main.html


urlpatterns = [
    path('main/', main_view, name='main'),
    path('itineraries/', itinerary_list, name='itinerary_list'),
    path('events/<str:event_id>/', event_details, name='event_details'),
    path('itineraries/create/', create_itinerary, name='create_itinerary'),
    path('itineraries/<int:itinerary_id>/', itinerary_detail, name='itinerary_detail'),
    path('itineraries/<int:itinerary_id>/update/', views.update_itinerary, name='update_itinerary'),
    path('itineraries/<int:itinerary_id>/delete/', views.delete_itinerary, name='delete_itinerary'),
    path('itineraries/<int:itinerary_id>/search-events/', search_park_events, name='search_park_events'),
    path('itineraries/<int:itinerary_id>/add-event/', add_event_to_itinerary, name='add_event_to_itinerary')
]