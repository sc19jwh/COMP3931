from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Include all of the landing app urls under base url /
    path('', include('apps.landing.urls')),
    # Include all of the trips app urls under base url /
    path('', include('apps.trips.urls')),
    # Include all user authentication urls
    path('user/', include('apps.authentication.urls')),
    # Include all currency urls
    path('currency/', include('apps.currencies.urls')),
    # Include all maps urls
    path('maps/', include('apps.maps.urls')),
    # Include all flights urls
    path('flights/', include('apps.flights.urls')),
    # Include admin page
    path('admin/', admin.site.urls),
]
