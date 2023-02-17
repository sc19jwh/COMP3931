# Django imports
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Folder imports
from .models import *

def cities(request):
    country = request.GET.get('country')
    cities = City.objects.filter(country=country)
    context = {'cities': cities}
    return render(request, 'partials/cities.html', context)