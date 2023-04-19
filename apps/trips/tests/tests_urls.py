from django.test import SimpleTestCase
from django.urls import resolve, reverse
from apps.trips.views import *

# Verify mapping between URLs and expected View Functions
class URLResolveTest(SimpleTestCase):

    def test_resolve_mytrips_url(self):
        url = reverse('mytrips', args=['jackhowkins'])
        self.assertEquals(resolve(url).func, mytrips)

    def test_resolve_configtrip_url(self):
        url = reverse('configtrip', args=['jackhowkins', 1])
        self.assertEquals(resolve(url).func, configtrip)

    def test_resolve_find_cities_url(self):
        url = reverse('find_cities')
        self.assertEquals(resolve(url).func, find_cities)

    def test_resolve_add_trip_url(self):
        url = reverse('add_trip')
        self.assertEquals(resolve(url).func, add_trip)

    def test_resolve_add_destination_url(self):
        url = reverse('add_destination')
        self.assertEquals(resolve(url).func, add_destination)

    def test_resolve_add_travel_url(self):
        url = reverse('add_travel')
        self.assertEquals(resolve(url).func, add_travel)

    def test_resolve_trip_summary_url(self):
        url = reverse('trip_summary')
        self.assertEquals(resolve(url).func, trip_summary)

    def test_resolve_journey_summary_url(self):
        url = reverse('journey_summary')
        self.assertEquals(resolve(url).func, journey_summary)

    def test_resolve_edit_destination_url(self):
        url = reverse('edit_destination')
        self.assertEquals(resolve(url).func, edit_destination)

    def test_resolve_edit_trip_details_url(self):
        url = reverse('edit_trip_details')
        self.assertEquals(resolve(url).func, edit_trip_details)

    def test_resolve_edit_travel_url(self):
        url = reverse('edit_travel')
        self.assertEquals(resolve(url).func, edit_travel)