# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
# Folder imports
from .models import *
from apps.authentication.models import Profile

def cities(request):
    country = request.GET.get('country')
    cities = City.objects.filter(country=country)
    context = {'cities': cities}
    return render(request, 'partials/cities.html', context)
