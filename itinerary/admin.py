from django.contrib import admin
from .models import Itinerary, Event

# Register your models here.
admin.site.register(Itinerary)
admin.site.register(Event)