from django.test import TestCase
from apps.trips.models import *
from apps.flights.models import *
from datetime import datetime, timedelta
from django.contrib.auth.models import User

class AirportModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name='Great Britain')
        self.city = City.objects.create(name='London', country=self.country)
        self.airport_name = "London Heathrow"
        self.airport_code = "LHR"
        self.lat = 1
        self.long = 2
        self.airport = Airport.objects.create(name=self.airport_name, country=self.country, iata_code=self.airport_code, longitude = self.long, latitude = self.lat)

    # Test that data stored data is the same as the data passed when creating
    def test_creation(self):
        self.assertEqual(self.airport.name, self.airport_name)
        self.assertEqual(self.airport.country, self.country)
        self.assertEqual(self.airport.iata_code, self.airport_code)
        self.assertEqual(self.airport.latitude, self.lat)
        self.assertEqual(self.airport.longitude, self.long)

    # Ensure that string representatinon of profile object is correct
    def test_string(self):
        self.assertEqual(str(self.airport), 'London Heathrow (LHR)')

class InterrailAirportModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name='Great Britain')
        self.city = City.objects.create(name='London', country=self.country)
        self.airport_name = "London Heathrow"
        self.airport_code = "LHR"
        self.lat = 1
        self.long = 2
        self.airport = Airport.objects.create(name=self.airport_name, country=self.country, iata_code=self.airport_code, longitude = self.long, latitude = self.lat)
        self.distance = 100
        self.interrail_airport = InterrailAirport.objects.create(city = self.city, airport = self.airport, distance = self.distance)

    # Test that data stored data is the same as the data passed when creating
    def test_creation(self):
        self.assertEqual(self.interrail_airport.airport, self.airport)
        self.assertEqual(self.interrail_airport.city, self.city)
        self.assertEqual(self.interrail_airport.distance, self.distance)

    # Ensure that string representatinon of profile object is correct
    def test_string(self):
        self.assertEqual(str(self.interrail_airport), 'London Heathrow - London')

class FlightModelTest(TestCase):
    def setUp(self):
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.country = Country.objects.create(name='Great Britain')
        self.city = City.objects.create(name='London', country=self.country)
        self.airport_name = "London Heathrow"
        self.airport_code = "LHR"
        self.lat = 1
        self.long = 2
        self.departure_airport = Airport.objects.create(name=self.airport_name, country=self.country, iata_code=self.airport_code, longitude = self.long, latitude = self.lat)
        self.arrival_airport = Airport.objects.create(name='London Gatwick', country=self.country, iata_code="GAT", longitude = 2, latitude = 3)
        self.trip = Trip.objects.create(user=self.user, title='London Trip')
        self.direction = 'inbound'
        self.departure_time = datetime.now()
        self.arrival_time = datetime.now() + timedelta(hours=4)
        self.duration = 120
        self.connections = 0
        self.flight = Flight.objects.create(
            direction=self.direction,
            trip=self.trip,
            departure_airport=self.departure_airport,
            arrival_airport=self.arrival_airport,
            departure_datetime=self.departure_time,
            arrival_datetime=self.arrival_time,
            duration=self.duration,
            number_connections=self.connections
        )

    # Test that data stored data is the same as the data passed when creating
    def test_creation(self):
        self.assertEqual(self.flight.direction, self.direction)
        self.assertEqual(self.flight.trip, self.trip)
        self.assertEqual(self.flight.departure_airport, self.departure_airport)
        self.assertEqual(self.flight.arrival_airport, self.arrival_airport)
        self.assertEqual(self.flight.departure_datetime, self.departure_time)
        self.assertEqual(self.flight.arrival_datetime, self.arrival_time)
        self.assertEqual(self.flight.duration, self.duration)
        self.assertEqual(self.flight.number_connections, self.connections)

    # Ensure that string representatinon of profile object is correct
    def test_string(self):
        self.assertEqual(str(self.flight), f"({self.username}) {self.trip.title}, {self.direction}")

    # Test timezone difference method works correctly
    def test_timezone(self):
        difference = self.flight.get_timezone_diff()
        self.assertEqual(difference.total_seconds() / 3600, 2)