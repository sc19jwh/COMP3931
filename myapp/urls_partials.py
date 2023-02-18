from django.urls import path
from . import views_partials

urlpatterns = [
    path('cities', views_partials.cities, name='cities'),
]