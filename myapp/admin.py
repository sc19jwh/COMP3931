from django.contrib import admin
from .models import *

# User-friendly database views for admin site
class CountryAdmin(admin.ModelAdmin):
    list_display= ('name', 'alpha2code', 'currency', 'is_interrail')

class CityAdmin(admin.ModelAdmin):
    list_display= ('name', 'country')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nationality')

class TripAdmin(admin.ModelAdmin):
    list_display= ('user', 'title')

class DestinationAdmin(admin.ModelAdmin):
    list_display= ('trip', 'country', 'city', 'start_date', 'end_date')

class TrainRouteAdmin(admin.ModelAdmin):
    list_display= ('start_city', 'end_city', 'duration')

class FerryRouteAdmin(admin.ModelAdmin):
    list_display= ('start_city', 'end_city', 'duration')
  
# Register models for editing in admin site
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(TrainRoute, TrainRouteAdmin)
admin.site.register(FerryRoute, FerryRouteAdmin)