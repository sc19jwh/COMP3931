import requests

def getExchangeRates(currency):
    response = requests.get('https://v6.exchangerate-api.com/v6/a915480af636a1707912d345/latest/' + currency)
    return response.json()['conversion_rates']