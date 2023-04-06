from django.test import SimpleTestCase
from django.urls import resolve, reverse
from apps.landing.views import *

class URLResolveTest(SimpleTestCase):

    def test_resolve_main_url(self):
        url = reverse('main')
        self.assertEquals(resolve(url).func, main)

    def test_resolve_features_url(self):
        url = reverse('features')
        self.assertEquals(resolve(url).func, features)

    def test_resolve_showcase1_url(self):
        url = reverse('showcase1')
        self.assertEquals(resolve(url).func, showcase1)

    def test_resolve_faqs_url(self):
        url = reverse('faqs')
        self.assertEquals(resolve(url).func, faqs)