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
]
