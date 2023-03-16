from django.db import models
from django.db.models import Min, Max
# Import default django User table
from django.contrib.auth.models import User

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
    skyscanner_id = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.name

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)

    def get_start_and_end_dates(self):
        start_date = self.destination_set.all().aggregate(Min('start_date'))['start_date__min']
        end_date = self.destination_set.all().aggregate(Max('end_date'))['end_date__max']
        return start_date, end_date

class Destination(models.Model):
    trip = models.ForeignKey("Trip", on_delete=models.CASCADE)
    country = models.ForeignKey("Country", on_delete=models.CASCADE)
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

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

    def __str__(self):
        return str(self.departure_destination.trip.id) + ": " + self.departure_destination.city.name + " - " + self.arrival_destination.city.name