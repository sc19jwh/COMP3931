from django.urls import include, path
from . import views_main as views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin', views.signin, name='signin'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('signout', views.signout, name='signout'),
    path('setcountry', views.setcountry, name='setcountry'),
    path('<str:username>/mytrips', views.mytrips, name='mytrips'),
    path('currency', views.currency, name='currency'),
    path('<str:username>/trip/<int:trip_id>', views.configtrip, name='configtrip')
]
