from django.test import TestCase, Client
from django.urls import resolve, reverse
from apps.trips.views import *
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import datetime

# Verify correct authorisation and redirection for urls
class ViewAuthRedirectTest(TestCase):
    def setUp(self):
        # Set up client
        self.client = Client()
        # Create first user account
        self.username = 'someusername'
        self.password = 'somepassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user)
        # Create a trip object
        self.trip = Trip.objects.create(
            user=self.user,
            title='Unit Test Trip',
            start_date='2024-03-01',
            journey_times=50,
            budget=50,
            climate=50,
            food_culture=50,
            tourist_attractions=50,
            nightlife_level=50
        )
        # Create a second user account
        self.alt_username = 'alternativeuser'
        self.alt_password = 'alternativepassword'
        self.alt_user = User.objects.create_user(username=self.alt_username, password=self.alt_password)
        self.alt_profile = Profile.objects.create(user=self.alt_user)

    # Log user in and make sure they can access <username>/mytrips
    def test_mytrips_url_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('mytrips', args=[self.username]))
        # Should return success
        self.assertEqual(response.status_code, 200)

    # Try to access <username>/mytrips without being logged in
    def test_mytrips_url_no_login(self):
        response = self.client.get(reverse('mytrips', args=[self.username]))
        # Should redirect
        self.assertEqual(response.status_code, 302)
        
    # Try to access <username>/mytrips while being logged in to a different account
    def test_mytrips_url_wrong_user(self):
        self.client.login(username=self.alt_username, password=self.alt_password)
        response = self.client.get(reverse('mytrips', args=[self.username]))
        # Should return unauthorised
        self.assertEqual(response.status_code, 401)

    # Log user in and make sure they can access <username>/trip/<trip_id>
    def test_config_trip_url_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('configtrip', args=[self.username, self.trip.id]))
        # Should return success
        self.assertEqual(response.status_code, 200)

    # Try to access <username>/trip/<trip_id> without being logged in
    def test_config_trip_url_no_login(self):
        response = self.client.get(reverse('configtrip', args=[self.username, self.trip.id]))
        # Should redirect
        self.assertEqual(response.status_code, 302)

    # Try to access <username>/trip/<trip_id> while being logged in to a different account
    def test_config_trip_url_wrong_user(self):
        self.client.login(username=self.alt_username, password=self.alt_password)
        response = self.client.get(reverse('configtrip', args=[self.username, self.trip.id]))
        # Should return unauthorised
        self.assertEqual(response.status_code, 401)

# Verify the functionality of mytrips
class MytripsFunctionalityTest(TestCase):
    def setUp(self):
        # Set up client
        self.client = Client()
        # Create first user account and login
        self.username = 'someusername'
        self.password = 'somepassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username=self.username, password=self.password)

    def test_add_trip(self):
        # Pass data to add trip
        data = {
            'add_trip_form': 'add_trip',
            'triptitle': 'Unit Test Trip',
            'start_date': '2024-03-01',
            'journeytime': '50.1',
            'budget': '40',
            'climate': '35',
            'food': '30.7',
            'tourism': '15.5',
            'nightlife': '12.4'
        }
        # POST data
        response = self.client.post(reverse('mytrips', args=[self.username]), data)
        # Get newly created trip
        trip = Trip.objects.get(user=self.user, title='Unit Test Trip')
        # Check that model exactly matches inputted data
        self.assertEqual(trip.start_date, datetime.strptime('2024-03-01', '%Y-%m-%d').date())
        self.assertEqual(trip.journey_times, Decimal('50.1'))
        self.assertEqual(trip.budget, Decimal('40'))
        self.assertEqual(trip.climate, Decimal('35'))
        self.assertEqual(trip.food_culture, Decimal('30.7'))
        self.assertEqual(trip.tourist_attractions, Decimal('15.5'))
        self.assertEqual(trip.nightlife_level, Decimal('12.4'))

    def test_delete_trip(self):
        # Temporarily create a Trip object
        trip = Trip.objects.create(
            user=self.user,
            title='Unit Test Trip',
            start_date='2024-03-01',
            journey_times=50.1,
            budget=40,
            climate=35,
            food_culture=30.7,
            tourist_attractions=15.5,
            nightlife_level=12.4
        )
        # Pass newly created trip's id
        data = {'delete_trip_form': trip.id}
        # POST the data
        response = self.client.post(reverse('mytrips', args=[self.username]), data)
        # Ensure that the delete has been performed
        with self.assertRaises(Trip.DoesNotExist):
            Trip.objects.get(id=trip.id)

# Verify the functionality of configtrip
class ConfigTripFunctionalityTest(TestCase):
    def setUp(self):
        # Set up client
        self.client = Client()
        # Create first user account and login
        self.username = 'someusername'
        self.password = 'somepassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username=self.username, password=self.password)