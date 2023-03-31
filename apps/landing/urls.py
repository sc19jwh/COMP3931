from django.urls import include, path
from . import views as views

urlpatterns = [
    path('main', views.main, name='main'),
    path('features', views.features, name='features'),
    path('showcase1', views.showcase1, name='showcase1'),
    path('faqs', views.faqs, name='faqs'),
    path('join', views.join, name='join'),
]
