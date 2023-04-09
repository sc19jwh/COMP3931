from django.test import SimpleTestCase
from django.urls import resolve, reverse
from apps.flights.views import *

# Verify mapping between URLs and expected View Functions
class URLResolveTest(SimpleTestCase):

    def test_resolve_add_flight_url(self):
        url = reverse('add_flight')
        self.assertEquals(resolve(url).func, add_flight)

    def test_resolve_enter_flight_url(self):
        url = reverse('enter_flight')
        self.assertEquals(resolve(url).func, enter_flight)

    def test_resolve_search_flight_url(self):
        url = reverse('search_flight')
        self.assertEquals(resolve(url).func, search_flight)

    def test_resolve_search_results_url(self):
        url = reverse('search_results')
        self.assertEquals(resolve(url).func, search_results)

    def test_resolve_airport_search_url(self):
        url = reverse('airport_search')
        self.assertEquals(resolve(url).func, airport_search)