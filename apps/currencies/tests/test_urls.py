from django.test import SimpleTestCase
from django.urls import resolve, reverse
from apps.currencies.views import *

class URLResolveTest(SimpleTestCase):

    def test_resolve_currency_url(self):
        url = reverse('currency')
        self.assertEquals(resolve(url).func, currency)

    def test_resolve_currency_conversion_url(self):
        url = reverse('currency_conversion')
        self.assertEquals(resolve(url).func, currency_conversion)
