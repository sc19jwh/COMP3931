from django.db import models
from django.contrib.auth.models import User
from apps.trips.models import Country

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.TextField(blank=True, null=True)
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='profiles', blank=True, null=True)

    def __str__(self):
        return self.user.username
