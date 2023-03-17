from django.contrib import admin
from .models import *

class AirportAdmin(admin.ModelAdmin):
    list_display= ('name', 'city', 'iata_code', 'distance')

class FlightAdmin(admin.ModelAdmin):
    list_display= ('direction', 'destination', 'departure_airport', 'arrival_airport', 'departure_datetime', 'arrival_datetime', 'duration')

class SubFlightAdmin(admin.ModelAdmin):
    list_display= ('master_flight', 'sub_departure_airport', 'sub_arrival_airport', 'sub_departure_datetime', 'sub_arrival_datetime', 'sub_duration', 'airline')

admin.site.register(Airport, AirportAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(SubFlight, SubFlightAdmin)