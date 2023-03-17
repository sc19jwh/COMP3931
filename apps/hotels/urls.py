from django.urls import include, path
from . import views as views

urlpatterns = [
    path('partials/search_hotel', views.search_hotel, name='search_hotel'),
]
