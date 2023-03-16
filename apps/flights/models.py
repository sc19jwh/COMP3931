from django.db import models
from apps.trips import models as trips_models

class Airport(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(trips_models.City, on_delete=models.CASCADE)
    iata_code = models.CharField(max_length=3)
    distance = models.DecimalField(max_digits=20, decimal_places=17)

    def __str__(self):
        return f"{self.name} ({self.iata_code}) - {self.city.name}"
