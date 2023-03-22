from django.db import models
# Import default django User table
from django.contrib.auth.models import User
# Import the trips tables
from apps.trips.models import *
# Import json
import json

class Hotel(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hotel_url = models.URLField()
    latitude = models.DecimalField(max_digits=20, decimal_places=17, blank=True, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=17, blank=True, null=True)
    star_rating = models.IntegerField(
        choices=[
            ('1', '*'),
            ('2', '**'),
            ('3', '***'),
            ('4', '****'),
            ('5', '*****'),
        ]
    )
    custom_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    image_urls = models.TextField(blank=True, null=True)

    def set_images(self, urls):
        self.image_urls = json.dumps(urls)

    def get_images(self):
        return json.loads(self.image_urls)

    def __str__(self):
        return f"{self.name} - {self.destination.city.name} ({self.destination.trip.user.username})"