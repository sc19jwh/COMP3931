from django.db import models
from django.db.models import Min, Max
# Import default django User table
from django.contrib.auth.models import User
# Other imports
from datetime import datetime, timedelta

class Country(models.Model):
    name = models.CharField(max_length=50)
    alpha2code = models.CharField(max_length=2)
    currency = models.CharField(max_length=3)
    is_interrail = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    photo_url = models.CharField(max_length=250, blank=True, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=17, blank=True, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=17, blank=True, null=True)
    accom_budget = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    food_budget = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    climate = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return self.name

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=25, blank=True, null=True)
    start_date = models.DateField(blank = True, null = True)
    journey_times = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    accom_budget = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    food_budget = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    climate = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

class Destination(models.Model):
    trip = models.ForeignKey("Trip", on_delete=models.CASCADE)
    country = models.ForeignKey("Country", on_delete=models.CASCADE)
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    nights = models.IntegerField(default=1)

    @property
    def start_date(self):
        if self.order == 1:
            return self.trip.start_date
        else:
            previous_destination = self.trip.destination_set.get(order=self.order-1)
            return previous_destination.end_date

    @property
    def end_date(self):
        start_date = self.start_date
        end_date = start_date + timedelta(days=self.nights)
        return end_date

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.trip.id} - {self.city.name}"
    
class TravelRoute(models.Model):
    start_city = models.ForeignKey("City", on_delete=models.CASCADE, related_name='start_travel_route')
    end_city = models.ForeignKey("City", on_delete=models.CASCADE, related_name='end_travel_route')
    duration = models.IntegerField()
    type = models.CharField(
        max_length=10,
        choices=[
            ('train', 'Train'),
            ('ferry', 'Ferry'),
            ('bus', 'Bus'),
        ]
    )

    def __str__(self):
        return self.start_city.name + " - " + self.end_city.name
    
class TransportLeg(models.Model):
    trip_transport = models.ForeignKey("DestinationTransport", on_delete=models.CASCADE, related_name="segments")
    route = models.ForeignKey("TravelRoute", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.trip_transport) + ", " + str(self.route)

class DestinationTransport(models.Model):
    departure_destination = models.ForeignKey("Destination", related_name="departure_destination", on_delete=models.CASCADE, default=1)
    arrival_destination = models.ForeignKey("Destination", related_name="arrival_destination", on_delete=models.CASCADE, default = 1)
    transport_legs = models.ManyToManyField(TransportLeg, blank=True)

    def get_route_array(self):
        route = []
        for leg in self.transport_legs.all():
            route.append(leg.route.start_city.name)
        route.append(self.arrival_destination.city.name)
        return route

    def __str__(self):
        return str(self.departure_destination.trip.id) + ": " + self.departure_destination.city.name + " - " + self.arrival_destination.city.name