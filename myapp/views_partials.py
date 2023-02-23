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

def set_country_flag(request):
    id = request.GET.get('country')
    country = Country.objects.get(id=id)
    context = {'countryid': country.alpha2code}
    return render(request, 'partials/set_country_flag.html', context)