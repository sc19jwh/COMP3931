from django.test import SimpleTestCase, TestCase, Client
from django.urls import resolve, reverse
from apps.trips.views import *
from django.contrib.auth.models import User

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

class URLUserAuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'someusername'
        self.password = 'somepassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user)
        self.trip = Trip.objects.create(
            user=self.user,
            title='title of trip',
            start_date='2024-03-01',
            journey_times=50,
            budget=50,
            climate=50,
            food_culture=50,
            tourist_attractions=50,
            nightlife_level=50
        )
        self.alt_username = 'alternativeuser'
        self.alt_password = 'alternativepassword'
        self.alt_user = User.objects.create_user(username=self.alt_username, password=self.alt_password)

    def test_mytrips_url_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('mytrips', args=[self.username]))
        self.assertEqual(response.status_code, 200)

    def test_mytrips_url_no_login(self):
        response = self.client.get(reverse('mytrips', args=[self.username]))
        self.assertEqual(response.status_code, 302)
        
    def test_mytrips_url_wrong_user(self):
        self.client.login(username=self.alt_username, password=self.alt_password)
        response = self.client.get(reverse('mytrips', args=[self.username]))
        self.assertEqual(response.status_code, 401)

    def test_config_trip_url_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('configtrip', args=[self.username, self.trip.id]))
        self.assertEqual(response.status_code, 200)

    def test_config_trip_url_no_login(self):
        response = self.client.get(reverse('configtrip', args=[self.username, self.trip.id]))
        self.assertEqual(response.status_code, 302)

    def test_config_trip_url_wrong_user(self):
        self.client.login(username=self.alt_username, password=self.alt_password)
        response = self.client.get(reverse('configtrip', args=[self.username, self.trip.id]))
        self.assertEqual(response.status_code, 401)