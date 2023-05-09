from django.urls import include, path
from . import views as views

urlpatterns = [
    path('<str:username>/mytrips', views.mytrips, name='mytrips'),
    path('<str:username>/trip/<int:trip_id>', views.configtrip, name='configtrip'),
    path('partials/find_cities', views.find_cities, name='find_cities'),
    path('partials/add_trip', views.add_trip, name='add_trip'),
    path('partials/add_destination', views.add_destination, name='add_destination'),
    path('partials/add_travel', views.add_travel, name='add_travel'),
    path('partials/trip_summary', views.trip_summary, name='trip_summary'),
    path('partials/journey_summary', views.journey_summary, name='journey_summary'),
    path('partials/edit_destination', views.edit_destination, name='edit_destination'),
    path('partials/edit_trip_details', views.edit_trip_details, name='edit_trip_details'),
    path('partials/edit_travel', views.edit_travel, name='edit_travel'),
]