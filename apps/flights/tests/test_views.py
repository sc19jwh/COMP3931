from django.test import TestCase, Client
from django.urls import resolve, reverse
from apps.flights.views import *
from apps.trips.models import Country
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import datetime

class FlightsTests(TestCase):
    def setUp(self):
        # Set up client
        self.client = Client()
        # Create first user account and login
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.profile = Profile.objects.create(user=self.user, nationality=self.country)
        self.client.login(username=self.username, password=self.password)
        # Create a trip, cities, airports and a flight for the trip
        self.trip = Trip.objects.create(user = self.user, title = "Test Trip", start_date = '2023-09-01')
        self.city1 = City.objects.create(name="London", country=self.country)
        self.city2 = City.objects.create(name="Bristol", country=self.country)
        self.travel_route = TravelRoute.objects.create(start_city = self.city1, end_city = self.city2, duration = 120, type = "train")
        self.airport1 = Airport.objects.create(name="London Heathrow", country=self.country, iata_code="LHR", longitude = 1, latitude = 1)
        self.airport2 = Airport.objects.create(name='London Gatwick', country=self.country, iata_code="GAT", longitude = 2, latitude = 3)
        self.interrail_airport1 = InterrailAirport.objects.create(airport = self.airport1, distance = 10, city = self.city1)
        self.interrail_airport2 = InterrailAirport.objects.create(airport = self.airport2, distance = 10, city = self.city1)
        self.flight = Flight.objects.create(
            direction='outbound',
            trip=self.trip,
            departure_airport=self.airport1,
            arrival_airport=self.airport2,
            departure_datetime=datetime.now(),
            arrival_datetime=datetime.now() + timedelta(hours=4),
            duration=240,
            number_connections=0
        )
        self.flight2 = Flight.objects.create(
            direction='inbound',
            trip=self.trip,
            departure_airport=self.airport2,
            arrival_airport=self.airport1,
            departure_datetime=datetime.now(),
            arrival_datetime=datetime.now() + timedelta(hours=4),
            duration=240,
            number_connections=0
        )
        self.destination1 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city1, order = 1, nights = 1)

    # Test that add flight pop up works correctly
    def test_add_flight_valid(self):
        response = self.client.get(reverse('add_flight'),
            {'flight_direction': 'outbound',
            'trip_id': self.trip.id}
        )
        self.assertEqual(response.status_code, 200)

    # Test that enter flight pop up works correctly
    def test_enter_flight_valid(self):
        response = self.client.get(reverse('enter_flight'),
            {'flight_direction': 'outbound',
            'trip_id': self.trip.id}
        )
        self.assertEqual(response.status_code, 200)

    # Test enter flight under incorrect trip id
    def test_enter_flight_invalid(self):
        response = self.client.get(reverse('enter_flight'),
            {'flight_direction': 'outbound',
            'trip_id': 190}
        )
        self.assertEqual(response.status_code, 404)

    # Test that search flight pop up works correctly for outbound flights
    def test_outbound_search_flight(self):
        response = self.client.get(reverse('search_flight'),
            {'flight_direction': 'outbound',
            'trip_id': self.trip.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['departure_airports'], Airport.objects.filter(country=self.profile.nationality).order_by('name'))
        self.assertQuerysetEqual(response.context['arrival_airports'], Airport.objects.all())

    # Test that search flight pop up works correctly for inbound flights
    def test_inbound_search_flight(self):
        response = self.client.get(reverse('search_flight'),
            {'flight_direction': 'inbound',
            'trip_id': self.trip.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['departure_airports'], Airport.objects.all())
        self.assertQuerysetEqual(response.context['arrival_airports'], Airport.objects.filter(country=self.profile.nationality).order_by('name'))

    # Test flight search on invalid flight search
    def test_searh_flight_invalid(self):
        response = self.client.get(reverse('search_flight'),
            {'flight_direction': 'inbound',
            'trip_id': 1000,
            'direct_flights': 'off'}
        )
        self.assertEqual(response.status_code, 404)

    # Test that search results pop up works correctly 
    def test_search_results_valid(self):
        response = self.client.get(reverse('search_results'),
            {'flight_direction': 'outbound',
            'departure_airport': self.airport1.id,
            'arrival_airport': self.airport2.id,
            'trip_id': self.trip.id,
            'direct_flights': 'on'}
        )
        self.assertEqual(response.status_code, 200)

    # Test that search results 404s for invalid trips 
    def test_search_results_invalid(self):
        response = self.client.get(reverse('search_results'),
            {'flight_direction': 'inbound',
            'departure_airport': self.airport1.id,
            'arrival_airport': self.airport2.id,
            'trip_id': 1000,
            'direct_flights': 'off'}
        )
        self.assertEqual(response.status_code, 404)