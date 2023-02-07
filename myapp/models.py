from django.db import models
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
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='profiles', default=1)

    def __str__(self):
        return self.user.username