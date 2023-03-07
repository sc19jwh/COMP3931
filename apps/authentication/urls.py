from django.urls import include, path
from apps.authentication import views

urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('signout', views.signout, name='signout'),
    path('setcountry', views.setcountry, name='setcountry'),
    path('partials/set_country_flag', views.set_country_flag, name='set_country_flag')
]
