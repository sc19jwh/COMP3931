from django.urls import include, path
from . import views as views

urlpatterns = [
    path('partials/add_flight', views.add_flight, name='add_flight'),
    path('partials/enter_flight', views.enter_flight, name='enter_flight'),
    path('partials/search_flight', views.search_flight, name='search_flight'),
    path('partials/search_results', views.search_results, name='search_results'),
]