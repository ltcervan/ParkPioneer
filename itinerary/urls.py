from django.urls import path
from . import views


urlpatterns = [
    path('main/', views.main_view, name='main'),
    path('itineraries/', views.itinerary_list, name='itinerary_list'),
    path('events/<str:event_id>/', views.event_details, name='event_details'),
    path('itineraries/create/', views.create_itinerary, name='create_itinerary'),
    path('itineraries/<int:itinerary_id>/', views.itinerary_detail, name='itinerary_detail'),
    path('itineraries/<int:itinerary_id>/update/', views.update_itinerary, name='update_itinerary'),
    path('itineraries/<int:itinerary_id>/delete/', views.delete_itinerary, name='delete_itinerary'),
    path('itineraries/<int:itinerary_id>/search-events/', views.search_park_events, name='search_park_events'),
    path('itineraries/<int:itinerary_id>/add-event/', views.add_event_to_itinerary, name='add_event_to_itinerary')
]