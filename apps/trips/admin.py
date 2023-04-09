from django.contrib import admin
from .models import *

# User-friendly database views for admin site
class CountryAdmin(admin.ModelAdmin):
    list_display= ('name', 'alpha2code', 'currency', 'is_interrail')

class CityAdmin(admin.ModelAdmin):
    list_display= ('name', 'country', 'skyscanner_id', 'latitude', 'longitude', 'photo_url', 'budget', 'climate', 'food_culture', 'tourist_attractions', 'nightlife_level')

class TripAdmin(admin.ModelAdmin):
    list_display= ('user', 'title', 'journey_times', 'budget', 'climate', 'food_culture', 'tourist_attractions', 'nightlife_level')

class DestinationAdmin(admin.ModelAdmin):
    list_display= ('trip', 'country', 'city')

class TravelRouteAdmin(admin.ModelAdmin):
    list_display= ('start_city', 'end_city', 'duration', 'type')
  
# Register models for editing in admin site
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(TravelRoute, TravelRouteAdmin)
admin.site.register(TransportLeg)
admin.site.register(DestinationTransport)