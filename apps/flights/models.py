from django.db import models
from apps.trips import models as trips_models

class Airport(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(trips_models.Country, on_delete=models.CASCADE, null=True)
    iata_code = models.CharField(max_length=3)
    latitude = models.DecimalField(max_digits=20, decimal_places=17, blank=True, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=17, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.iata_code})"
    
class InterrailAirport(models.Model):
    city = models.ForeignKey(trips_models.City, on_delete=models.CASCADE, null=True)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, null=True)
    distance = models.DecimalField(max_digits=20, decimal_places=17, blank=True, null=True)
    
    def __str__(self):
        return f"{self.airport.name} - {self.city.name}"

class Flight(models.Model):
    direction = models.CharField(
        max_length=10,
        choices=[
            ('outbound', 'Outbound'),
            ('inbound', 'Inbound')
        ]
    )
    trip = models.ForeignKey(trips_models.Trip, on_delete=models.CASCADE, default=5)
    departure_airport = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name='departure_airport')
    arrival_airport = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name='arrival_airport')
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    duration = models.IntegerField()
    number_connections = models.IntegerField(default=0)

    def __str__(self):
        return f"({self.trip.user.username}) {self.trip.title}, {self.direction}"