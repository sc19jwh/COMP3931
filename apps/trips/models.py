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

    def __str__(self):
        return self.start_city.name + " - " + self.end_city.name