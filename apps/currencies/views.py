from django.shortcuts import render
from apps.trips.models import Country
from apps.authentication.models import Profile
from .utils.currency import getExchangeRates
from apps.authentication.decorators import nationality_required
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
import os

# URL: /currency/
# HTTP Method: GET
# Description: Template for currency conversion form
@login_required(redirect_field_name=None)
@nationality_required
def currency(request):
    countries = Country.objects.all()
    interrail_countries = Country.objects.filter(is_interrail=True)
    load_dotenv()
    currency_key = os.getenv('currency_api_key')
    if currency_key:
        key_found = True
    else:
        key_found = False
    context = {'title': 'Currency', 'countries': countries, 'interrail_countries': interrail_countries, 'profile': Profile.objects.get(user=request.user),
               'selected_page': 'Currency', 'middle': True, 'key_found': key_found}
    return render(request, 'conversion.html', context)

# URL: currency/partials/currency_conversion
# HTTP Method: POST
# Description: Converts entered amount between start and end currencies
def currency_conversion(request):
    # Retrieve currencies from the selected fields
    if request.method == 'POST':
        start_currency = Country.objects.get(id=request.POST.get('country')).currency
        result_currency = Country.objects.get(id=request.POST.get('country2')).currency
        amount = request.POST.get('amount')
        formatted_amount = "{:.2f}".format(round(float(amount), 2))
        conversion = getExchangeRates(start_currency)[result_currency] * float(amount)
        formatted_conversion = "{:.2f}".format(round(conversion, 2))
        context = {'profile': Profile.objects.get(user=request.user), 'start_currency': start_currency, 'result_currency': result_currency, 'conversion': formatted_conversion, 'amount': formatted_amount}
        return render(request, 'partials/result.html', context)