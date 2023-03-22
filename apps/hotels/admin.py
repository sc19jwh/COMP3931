from django.contrib import admin
from .models import *

# User-friendly database views for admin site
class HotelAdmin(admin.ModelAdmin):
    list_display= ('destination', 'name')
  
# Register models for editing in admin site
admin.site.register(Hotel, HotelAdmin)