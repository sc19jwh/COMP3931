import requests
from dotenv import load_dotenv
import os

def getExchangeRates(currency):
    load_dotenv()
    api_key = os.getenv('currency_api_key')
    response = requests.get(f'https://v6.exchangerate-api.com/v6/{api_key}/latest/' + currency)
    return response.json()['conversion_rates']