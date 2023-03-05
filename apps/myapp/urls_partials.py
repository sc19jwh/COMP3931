from django.urls import path
from . import views_partials as views

urlpatterns = [
    path('cities', views.cities, name='cities'),
]