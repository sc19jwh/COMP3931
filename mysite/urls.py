from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Include all of the main app urls under base url /
    path('', include('apps.myapp.urls')),
    # Include all user authentication urls
    path('user/', include('apps.authentication.urls')),
    # Include all currency urls
    path('currency/', include('apps.currencies.urls')),
    # Include admin page
    path('admin/', admin.site.urls),
]
