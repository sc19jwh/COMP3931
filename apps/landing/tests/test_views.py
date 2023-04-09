from django.test import TestCase, Client
from django.urls import resolve, reverse
from apps.landing.views import *
from django.contrib.auth.models import User
from apps.trips.models import Country

class LandingTests(TestCase):
    def setUp(self):
        # Set up client
        self.client = Client()
        # Create a test account
        self.username = 'someusername'
        self.email = 'someusername@email.com'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email)
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.profile = Profile.objects.create(user=self.user, nationality=self.country)

    def test_main_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('main'))
        self.assertRedirects(response, reverse('mytrips', args=[self.username]))

    def test_main_guest(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_faqs(self):
        response = self.client.get(reverse('faqs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/faqs.html')

    def test_features(self):
        response = self.client.get(reverse('features'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/features.html')

    def test_showcase1(self):
        response = self.client.get(reverse('showcase1'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/showcase1.html')