from django.contrib import admin
from .models import *

class AirportAdmin(admin.ModelAdmin):
    list_display= ('name', 'city', 'iata_code', 'distance')

admin.site.register(Airport, AirportAdmin)