from django.test import SimpleTestCase
from django.urls import resolve, reverse
from apps.authentication.views import *

# Verify mapping between URLs and expected View Functions
class URLResolveTest(SimpleTestCase):

    def test_resolve_signin_url(self):
        url = reverse('signin')
        self.assertEquals(resolve(url).func, signin)

    def test_resolve_register_url(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_resolve_profile_url(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile)

    def test_resolve_signout_url(self):
        url = reverse('signout')
        self.assertEquals(resolve(url).func, signout)

    def test_resolve_setcountry_url(self):
        url = reverse('setcountry')
        self.assertEquals(resolve(url).func, setcountry)

    def test_resolve_set_country_flag_url(self):
        url = reverse('set_country_flag')
        self.assertEquals(resolve(url).func, set_country_flag)