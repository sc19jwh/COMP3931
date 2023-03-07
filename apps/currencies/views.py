from django.shortcuts import render
from apps.myapp.models import Country
from apps.authentication.models import Profile
from .utils.currency import getExchangeRates

def currency(request):
    countries = Country.objects.all()
    interrail_countries = Country.objects.filter(is_interrail=True)
    context = {'title': 'Currency', 'countries': countries, 'interrail_countries': interrail_countries, 'profile': Profile.objects.get(user=request.user)}
    return render(request, 'conversion.html', context)

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