from django.urls import include, path
from . import views as views

urlpatterns = [
    path('main', views.main, name='main'),
    path('partials/features', views.features, name='features'),
    path('partials/showcase1', views.showcase1, name='showcase1'),
    path('partials/faqs', views.faqs, name='faqs'),
]
