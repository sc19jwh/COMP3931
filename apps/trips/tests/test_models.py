from django.test import TestCase
from apps.trips.models import *
from apps.flights.models import *
from django.contrib.auth.models import User

class CountryModelTest(TestCase):
    def setUp(self):
        self.name = "Great Britain"
        self.alpha2code = "GB"
        self.currency = "GBP"
        self.is_interrail = False
        self.country = Country.objects.create(name=self.name, alpha2code = self.alpha2code, currency = self.currency,
                                              is_interrail = self.is_interrail)

    # Test that data stored data is the same as the data passed when creating
    def test_creation(self):
        self.assertEqual(self.country.name, self.name)
        self.assertEqual(self.country.alpha2code, self.alpha2code)
        self.assertEqual(self.country.currency, self.currency)
        self.assertEqual(self.country.is_interrail, self.is_interrail)

    # Ensure that string representatinon of profile object is correct
    def test_string(self):
        self.assertEqual(str(self.country), self.name)

class CityModelTest(TestCase):
    def setUp(self):
        self.country_name = "Great Britain"
        self.alpha2code = "GB"
        self.currency = "GBP"
        self.is_interrail = False
        self.country = Country.objects.create(name=self.country_name, alpha2code = self.alpha2code, currency = self.currency,
                                              is_interrail = self.is_interrail)
        self.city_name = "London"
        self.photo_url = "url"
        self.longitude = 1
        self.latitude = 1
        self.budget = 10
        self.climate = 20
        self.food_culture = 30
        self.tourist_attractions = 40
        self.nightlife_level = 50
        self.city = City.objects.create(name = self.city_name, country = self.country, photo_url = self.photo_url,
                                        longitude = self.longitude, latitude = self.latitude, budget = self.budget,
                                        climate = self.climate, food_culture = self.food_culture, tourist_attractions = 
                                        self.tourist_attractions, nightlife_level = self.nightlife_level)

    # Test that data stored data is the same as the data passed when creating
    def test_creation(self):
        self.assertEqual(self.city.name, self.city_name)
        self.assertEqual(self.city.photo_url, self.photo_url)
        self.assertEqual(self.city.longitude, self.longitude)
        self.assertEqual(self.city.latitude, self.latitude)
        self.assertEqual(self.city.budget, self.budget)
        self.assertEqual(self.city.climate, self.climate)
        self.assertEqual(self.city.food_culture, self.food_culture)
        self.assertEqual(self.city.tourist_attractions, self.tourist_attractions)
        self.assertEqual(self.city.nightlife_level, self.nightlife_level)

    # Ensure that string representatinon of profile object is correct
    def test_string(self):
        self.assertEqual(str(self.city), self.city_name)

class TripModelTest(TestCase):
    def setUp(self):
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.title = "Trip 1"
        self.start_date = "2024-01-02"
        self.journey_times = 5
        self.budget = 10
        self.climate = 20
        self.food_culture = 30
        self.tourist_attractions = 40
        self.nightlife_level = 50
        self.trip = Trip.objects.create(user = self.user, title = self.title, start_date = self.start_date,
                                        journey_times = self.journey_times, budget = self.budget,
                                        climate = self.climate, food_culture = self.food_culture, tourist_attractions = 
                                        self.tourist_attractions, nightlife_level = self.nightlife_level)

    # Test that data stored data is the same as the data passed when creating
    def test_creation(self):
        self.assertEqual(self.trip.user, self.user)
        self.assertEqual(self.trip.title, self.title)
        self.assertEqual(self.trip.start_date, self.start_date)
        self.assertEqual(self.trip.journey_times, self.journey_times)
        self.assertEqual(self.trip.budget, self.budget)
        self.assertEqual(self.trip.climate, self.climate)
        self.assertEqual(self.trip.food_culture, self.food_culture)
        self.assertEqual(self.trip.tourist_attractions, self.tourist_attractions)
        self.assertEqual(self.trip.nightlife_level, self.nightlife_level)

class DestinationModelTest(TestCase):
    def setUp(self):
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.country = Country.objects.create(name="Great Britain")
        self.city1 = City.objects.create(name="London", country=self.country)
        self.city2 = City.objects.create(name="Bristol", country=self.country)
        self.city3 = City.objects.create(name="Birmingham", country=self.country)
        self.trip = Trip.objects.create(user = self.user, title = 'Trip 1', start_date=datetime.now())
        self.destination1 = Destination.objects.create(trip=self.trip, country=self.country, city=self.city1, order=3, nights=1)
        self.destination2 = Destination.objects.create(trip=self.trip, country=self.country, city=self.city2, order=2, nights=2)
        self.destination3 = Destination.objects.create(trip=self.trip, country=self.country, city=self.city3, order=1, nights=3)

    # Test that data stored data is the same as the data passed when creating
    def test_creation(self):
        self.assertEqual(self.destination1.trip, self.trip)
        self.assertEqual(self.destination1.country, self.country)
        self.assertEqual(self.destination1.city, self.city1)
        self.assertEqual(self.destination1.order, 3)
        self.assertEqual(self.destination1.nights, 1)

    # Ensure that start_date property works correctly
    def test_start_date(self):
        self.assertEqual(self.destination3.start_date, self.trip.start_date)
        self.assertEqual(self.destination2.start_date, self.destination3.end_date)
        self.assertEqual(self.destination1.start_date, self.destination2.end_date)

    # Ensure that end_date property works correctly
    def test_end_date(self):
        self.assertEqual(self.destination1.end_date, self.destination1.start_date + timedelta(days=self.destination1.nights))

    # Ensure that string representatinon of profile object is correct
    def test_str(self):
        self.assertEqual(str(self.destination1), f"{self.trip.id} - {self.city1.name}")

class TravelRouteModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Great Britain")
        self.city1 = City.objects.create(name="London", country=self.country)
        self.city2 = City.objects.create(name="Bristol", country=self.country)
        self.duration = 100
        self.type = 'train'
        self.route = TravelRoute.objects.create(start_city = self.city1, end_city = self.city2, duration = self.duration,
                                                type = self.type)
        
    # Test that data stored data is the same as the data passed when creating
    def test_creation(self):
        self.assertEqual(self.route.start_city, self.city1)
        self.assertEqual(self.route.end_city, self.city2)
        self.assertEqual(self.route.duration, self.duration)
        self.assertEqual(self.route.type, self.type)

    # Ensure that string representatinon of profile object is correct
    def test_str(self):
        self.assertEqual(str(self.route), f"{self.route.start_city.name} - {self.route.end_city.name}")

class DestinationTransportModelTest(TestCase):
    def setUp(self):
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.country = Country.objects.create(name="Great Britain")
        self.city1 = City.objects.create(name="London", country=self.country)
        self.city2 = City.objects.create(name="Bristol", country=self.country)
        self.trip = Trip.objects.create(user = self.user, title = 'Trip 1', start_date=datetime.now())
        self.destination1 = Destination.objects.create(trip=self.trip, country=self.country, city=self.city1, order=3, nights=1)
        self.destination2 = Destination.objects.create(trip=self.trip, country=self.country, city=self.city2, order=2, nights=2)
        self.destination_transport = DestinationTransport.objects.create(departure_destination = self.destination1, arrival_destination = self.destination2)
        self.route = TravelRoute.objects.create(start_city = self.city1, end_city = self.city2, duration = 100,
                                                type = 'train')
        self.transport_leg = TransportLeg.objects.create(trip_transport = self.destination_transport, route = self.route)

    # Test that data stored data is the same as the data passed when creating
    def test_creation(self):
        self.assertEqual(self.destination_transport.departure_destination, self.destination1)
        self.assertEqual(self.destination_transport.arrival_destination, self.destination2)

    # Ensure that string representatinon of profile object is correct
    def test_str(self):
        self.assertEqual(str(self.destination_transport), f"{str(self.destination_transport.departure_destination.trip.id)}: {self.destination_transport.departure_destination.city.name} - {self.destination_transport.arrival_destination.city.name}")

    # Test that the get route array method works correctly
    def test_get_route_array(self):
        self.assertEqual(self.destination_transport.get_route_array(), [self.route.end_city.name])

class TransportLegModelTest(TestCase):
    def setUp(self):
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.country = Country.objects.create(name="Great Britain")
        self.city1 = City.objects.create(name="London", country=self.country)
        self.city2 = City.objects.create(name="Bristol", country=self.country)
        self.trip = Trip.objects.create(user = self.user, title = 'Trip 1', start_date=datetime.now())
        self.destination1 = Destination.objects.create(trip=self.trip, country=self.country, city=self.city1, order=3, nights=1)
        self.destination2 = Destination.objects.create(trip=self.trip, country=self.country, city=self.city2, order=2, nights=2)
        self.destination_transport = DestinationTransport.objects.create(departure_destination = self.destination1, arrival_destination = self.destination2)
        self.route = TravelRoute.objects.create(start_city = self.city1, end_city = self.city2, duration = 100,
                                                type = 'train')
        self.transport_leg = TransportLeg.objects.create(trip_transport = self.destination_transport, route = self.route)

    # Test that data stored data is the same as the data passed when creating
    def test_creation(self):
        self.assertEqual(self.transport_leg.trip_transport, self.destination_transport)
        self.assertEqual(self.transport_leg.route, self.route)

    # Ensure that string representatinon of profile object is correct
    def test_str(self):
        self.assertEqual(str(self.transport_leg), f"{str(self.transport_leg.trip_transport)}, {str(self.transport_leg.route)}")