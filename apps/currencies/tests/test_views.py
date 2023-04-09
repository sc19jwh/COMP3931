from django.test import TestCase, Client
from django.urls import resolve, reverse
from apps.authentication.views import *
from django.contrib.auth.models import User
from apps.trips.models import Country
from apps.currencies.utils.currency import getExchangeRates

# Verify correct authorisation and redirection for urls
class ViewAuthRedirectTest(TestCase):
    def setUp(self):
        # Set up client
        self.client = Client()
        # Create first user account
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.profile = Profile.objects.create(user=self.user, nationality=self.country)

    # Make sure a guest can access user/signin
    def test_currency_guest(self):
        response = self.client.get(reverse('currency'))
        self.assertRedirects(response, reverse('signin'))

    def test_currency_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('currency'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversion.html')

# Verify the functionality of currency conversion
class CurrencyFunctionalityTests(TestCase):
    def setUp(self):
        # Set up client
        self.client = Client()
        # Create first user account and login
        self.username = 'someusername'
        self.email = 'someusername@email.com'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email)
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.second_country = Country.objects.create(name = "Spain", alpha2code = "ES", currency = "EUR", is_interrail = True)
        self.profile = Profile.objects.create(user=self.user, nationality=self.country)
        self.client.login(username=self.username, password=self.password)

    # Test currency page to ensure that the user's national currency is used as default 
    # Currency code should appear four times on page load (twice in the input boxes and twice in the result)
    def test_default_currency(self):
        response = self.client.get(reverse('currency'))
        self.assertContains(response, self.profile.nationality.currency, count=4)

    # Test the conversion of two currencies by passing the values to the view and manually to the conversion function and ensuring the same result
    def test_currency_conversion(self):
        response = self.client.post(reverse('currency_conversion'), {'country': self.country.id, 'country2': self.second_country.id, 'amount': '150'})
        conversion_rate = getExchangeRates(self.country.currency)[self.second_country.currency]
        function_result = round(150 * conversion_rate, 2)
        self.assertEqual(float(response.context['conversion']), function_result)