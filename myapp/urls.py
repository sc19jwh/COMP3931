from django.urls import path
from . import views
from . import views_partials

urlpatterns = [
    path('', views.home, name='home'),
    path('signin', views.signin, name='signin'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('signout', views.signout, name='signout'),
    path('setcountry', views.setcountry, name='setcountry'),
    path('mytrips', views.mytrips, name='mytrips'),
    path('cities', views_partials.cities, name='cities'),
]
