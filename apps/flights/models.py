from django.db import models
from apps.trips import models as trips_models

class Airport(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(trips_models.City, on_delete=models.CASCADE)
    iata_code = models.CharField(max_length=3)
    distance = models.DecimalField(max_digits=20, decimal_places=17)

    def __str__(self):
        return f"{self.name} ({self.iata_code}) - {self.city.name}"
    
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

    def __str__(self):
        return f"({self.trip.user.username}) {self.trip.title}, {self.direction}"

class SubFlight(models.Model):
    master_flight = models.ForeignKey("Flight", on_delete=models.CASCADE)
    sub_departure_airport = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name='sub_departure_airport')
    sub_arrival_airport = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name='sub_arrival_airport')
    sub_departure_datetime = models.DateTimeField()
    sub_arrival_datetime = models.DateTimeField()
    sub_duration = models.IntegerField()

    def __str__(self):
        return f"{self.master_flight} ({self.sub_departure_airport.city.name} - {self.sub_arrival_airport.city.name})"