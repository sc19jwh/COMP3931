from django.urls import include, path
from . import views as views

urlpatterns = [
    path('', views.currency, name='currency'),
    path('partials/currency_conversion', views.currency_conversion, name='currency_conversion'),
]
