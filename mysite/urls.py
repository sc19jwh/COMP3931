from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Include all of the main app urls under base url /
    path('', include('myapp.urls_main')),
    # Include all of the partials paths under partials/...
    path('partials/', include('myapp.urls_partials')),
    # Include admin page
    path('admin/', admin.site.urls),
]
