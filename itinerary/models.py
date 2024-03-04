from django.utils import timezone
from django.conf import settings
from django.db import models
import uuid

class Itinerary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='itineraries')
    park_title = models.CharField(max_length=200)
    title = models.CharField(max_length=200, default='Untitled Itinerary')
    start_date = models.DateField()
    end_date = models.DateField()
    event = models.TextField()

    def __str__(self):
        return f"{self.park_title} from {self.start_date} to {self.end_date}"

    def is_upcoming(self):
        return self.start_date > timezone.now().date()

    def is_past(self):
        return self.end_date < timezone.now().date()
    

class Event(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='events')
    event_id = models.CharField(max_length=36, unique=True, primary_key=True)
    title = models.CharField(max_length=200)
    time = models.TimeField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    fee = models.CharField(max_length=100, blank=True, null=True)  
    description = models.TextField(blank=True, null=True)
    is_repeating = models.BooleanField(default=False)
    registration_required = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} on {self.date} at {self.time}, {self.location}"



