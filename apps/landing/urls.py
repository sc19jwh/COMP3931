from django.urls import include, path
from . import views as views

urlpatterns = [
    path('', views.main, name='main'),
    path('credits', views.credits, name='credits'),
    path('partials/faqs', views.faqs, name='faqs'),
]
