from django.contrib import admin
from .models import *

class AirportAdmin(admin.ModelAdmin):
    list_display= ('name', 'country', 'iata_code', 'latitude', 'longitude')

class InterrailAirportAdmin(admin.ModelAdmin):
    list_display= ('airport', 'city', 'distance')

class FlightAdmin(admin.ModelAdmin):
    list_display= ('direction', 'trip', 'departure_airport', 'arrival_airport', 'departure_datetime', 'arrival_datetime', 'duration', 'number_connections')

admin.site.register(Airport, AirportAdmin)
admin.site.register(InterrailAirport, InterrailAirportAdmin)
admin.site.register(Flight, FlightAdmin)