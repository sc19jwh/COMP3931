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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.TextField(blank=True, null=True)
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='profiles', blank=True, null=True)

    def __str__(self):
        return self.user.username

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
    city = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()