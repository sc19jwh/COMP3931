from django.urls import path
from . import views_partials as views

urlpatterns = [
    path('cities', views.cities, name='cities'),
    path('set_country_flag', views.set_country_flag, name='set_country_flag'),
    path('currency', views.currency_conversion, name='currency_conversion'),
]