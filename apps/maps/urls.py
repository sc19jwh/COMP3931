from django.urls import include, path
from . import views as views

urlpatterns = [
    path('partials/full_map', views.full_map, name='full_map'),
    path('partials/get_travel_map', views.get_travel_map, name='get_travel_map'),
    path('partials/get_route_map', views.get_route_map, name='get_route_map'),
]
