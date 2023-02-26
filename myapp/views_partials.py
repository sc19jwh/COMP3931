# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
# Folder imports
from .models import *
from .utils.currency import *

def cities(request):
    country = request.GET.get('country')
    cities = City.objects.filter(country=country)
    context = {'cities': cities}
    return render(request, 'partials/cities.html', context)

def set_country_flag(request):
    id = request.GET.get('country')
    if not id:
        id = request.GET.get('country2')
    country = Country.objects.get(id=id)
    context = {'countryid': country.alpha2code}
    return render(request, 'partials/set_country_flag.html', context)

def currency_conversion(request):
    # Retrieve currencies from the selected fields
    if request.method == 'POST':
        start_currency = Country.objects.get(id=request.POST.get('country')).currency
        result_currency = Country.objects.get(id=request.POST.get('country2')).currency
    conversion = getExchangeRates(start_currency)[result_currency]
    formatted_conversion = "{:.2f}".format(round(conversion, 2))
    context = {'profile': Profile.objects.get(user=request.user), 'start_currency': start_currency, 'result_currency': result_currency, 'conversion': formatted_conversion}
    return render(request, 'partials/currency_conversion.html', context)
