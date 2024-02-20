from django.db import models
from django.conf import settings
from django.utils import timezone

class Itinerary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='itineraries')
    park_title = models.CharField(max_length=200)
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
    title = models.CharField(max_length=200)
    time = models.TimeField()
    date = models.DateField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} on {self.date} at {self.time}, {self.location}"



