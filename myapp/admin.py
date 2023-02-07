from django.contrib import admin
from .models import *

class CountryAdmin(admin.ModelAdmin):
    list_display= ('name', 'alpha2code', 'currency', 'is_interrail')

class CityAdmin(admin.ModelAdmin):
    list_display= ('name', 'country')

class ProfileAdmin(admin.ModelAdmin):
    list_display= ('user', 'nationality', 'image')
  
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Profile, ProfileAdmin)