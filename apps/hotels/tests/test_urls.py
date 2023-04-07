from django.test import SimpleTestCase
from django.urls import resolve, reverse
from apps.hotels.views import *

# Verify mapping between URLs and expected View Functions
class URLResolveTest(SimpleTestCase):

    def test_resolve_search_hotel_url(self):
        url = reverse('search_hotel')
        self.assertEquals(resolve(url).func, search_hotel)