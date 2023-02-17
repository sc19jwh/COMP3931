from django.contrib import admin
from .models import *

class CountryAdmin(admin.ModelAdmin):
    list_display= ('name', 'alpha2code', 'currency', 'is_interrail')

class CityAdmin(admin.ModelAdmin):
    list_display= ('name', 'country')
  
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Profile)
admin.site.register(Trip)
admin.site.register(Destination)