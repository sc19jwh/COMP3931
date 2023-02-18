from django.urls import include, path
from . import views_main

urlpatterns = [
    path('', views_main.home, name='home'),
    path('signin', views_main.signin, name='signin'),
    path('register', views_main.register, name='register'),
    path('profile', views_main.profile, name='profile'),
    path('signout', views_main.signout, name='signout'),
    path('setcountry', views_main.setcountry, name='setcountry'),
    path('mytrips', views_main.mytrips, name='mytrips'),
    path('partials/', include('myapp.urls_partials')),
]
