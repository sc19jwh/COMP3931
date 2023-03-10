from django.urls import include, path
from . import views as views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:username>/mytrips', views.mytrips, name='mytrips'),
    path('<str:username>/trip/<int:trip_id>', views.configtrip, name='configtrip'),
    path('partials/find_cities', views.find_cities, name='find_cities'),
    path('partials/dependent_dates', views.dependent_dates, name='dependent_dates'),
    path('partials/add_trip', views.add_trip, name='add_trip'),
    path('partials/add_destination', views.add_destination, name='add_destination'),
    path('partials/add_travel', views.add_travel, name='add_travel'),
    path('partials/full_map', views.full_map, name='full_map'),
    path('partials/get_travel_map', views.get_travel_map, name='get_travel_map'),
    path('partials/get_route_map', views.get_route_map, name='get_route_map'),
]
