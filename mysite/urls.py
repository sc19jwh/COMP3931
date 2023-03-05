from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Include all of the main app urls under base url /
    path('', include('apps.myapp.urls_main')),
    # Include all user authentication urls
    path('user/', include('apps.authentication.urls')),
    # Include all currency urls
    path('currency/', include('apps.currencies.urls')),
    # Include all of the partials paths under partials/...
    path('partials/', include('apps.myapp.urls_partials')),
    # Include admin page
    path('admin/', admin.site.urls),
]
