from django.urls import path
from . import views
from .views import main_view  # Replace with your actual view that renders main.html


urlpatterns = [
    path('main/', main_view, name='main'),
    path('itineraries/', views.itinerary_list, name='itinerary_list')
]