from django.urls import include, path
from . import views_main as views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:username>/mytrips', views.mytrips, name='mytrips'),
    path('<str:username>/trip/<int:trip_id>', views.configtrip, name='configtrip')
]
