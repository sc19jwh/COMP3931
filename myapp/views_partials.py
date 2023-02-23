# Django imports
from django.shortcuts import render, redirect
from django.http import HttpResponse
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
    # Initially default start and end currencies to users nationality
    start_currency = Profile.objects.get(user=request.user).nationality.currency
    result_currency = Profile.objects.get(user=request.user).nationality.currency
    # Then get currencies from the selected fields
    # start_currency = request.GET.get('country')
    # result_currency = Country.objects.get(id=id).currency
    conversion = getExchangeRates(start_currency)[result_currency]
    context = {'start_currency': start_currency, 'result_currency': result_currency, 'conversion': conversion}
    return render(request, 'partials/currency_conversion.html', context)