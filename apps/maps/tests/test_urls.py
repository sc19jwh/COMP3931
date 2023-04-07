from django.test import SimpleTestCase
from django.urls import resolve, reverse
from apps.maps.views import *

# Verify mapping between URLs and expected View Functions
class URLResolveTest(SimpleTestCase):

    def test_resolve_full_map_url(self):
        url = reverse('full_map')
        self.assertEquals(resolve(url).func, full_map)

    def test_resolve_get_travel_map_url(self):
        url = reverse('get_travel_map')
        self.assertEquals(resolve(url).func, get_travel_map)

    def test_resolve_get_route_map_url(self):
        url = reverse('get_route_map')
        self.assertEquals(resolve(url).func, get_route_map)

    def test_resolve_get_hotels_map_url(self):
        url = reverse('get_hotels_map')
        self.assertEquals(resolve(url).func, get_hotels_map)

    def test_resolve_get_trip_map_url(self):
        url = reverse('get_trip_map')
        self.assertEquals(resolve(url).func, get_trip_map)