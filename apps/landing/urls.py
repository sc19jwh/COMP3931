from django.urls import include, path
from . import views as views

urlpatterns = [
    path('test', views.test, name='test'),
]
