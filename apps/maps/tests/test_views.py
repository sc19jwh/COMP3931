from django.test import TestCase, Client
from django.urls import resolve, reverse
from apps.maps.views import *
from django.contrib.auth.models import User
from apps.authentication.models import Profile
from apps.trips.models import *

class MapsTests(TestCase):
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
        self.city1 = City.objects.create(name = "London", country = self.country, latitude = 51.5073359, longitude = -0.12765)
        # Create test cities, destinations and trip
        self.city2 = City.objects.create(name = "Birmingham", country = self.country, latitude = 52.4796992, longitude = -1.9026911)
        self.city3 = City.objects.create(name = "Edinburgh", country = self.country, latitude = 55.9533456, longitude = -3.1883749)
        self.city4 = City.objects.create(name = "Penzance", country = self.country, latitude = 50.1194794, longitude = -5.5352463)
        self.trip = Trip.objects.create(user=self.user)
        self.destination1 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city1, order = 1, nights = 1)
        self.destination2 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city2, order = 2, nights = 1)
        self.destination3 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city3, order = 3, nights = 1)
        self.destination4 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city4, order = 4, nights = 1)
        self.travelroute1 = TravelRoute.objects.create(start_city = self.city1, end_city = self.city2, duration = 105, type = 'train')
        self.travelroute1 = TravelRoute.objects.create(start_city = self.city2, end_city = self.city3, duration = 265, type = 'train')
        self.client.login(username=self.username, password=self.password)

    # Test that the view works by providing valid input parameters
    def test_travel_map_valid(self):
        response = self.client.get(reverse('get_travel_map'), {'start': self.destination1.id, 'end': self.destination2.id})
        self.assertEqual(response.status_code, 200)

    # Test that the view handles passing destination parameters where no destination exists
    def test_travel_map_invalid(self):
        response = self.client.get(reverse('get_travel_map'), {'start': 15, 'end': 25})
        self.assertEqual(response.status_code, 404)

    # Test that the view returns a bad request when no parameters are passed
    def test_travel_map_no_params(self):
        response = self.client.get(reverse('get_travel_map'))
        self.assertEqual(response.status_code, 400)

    # Test route map by passing valid cities 
    def test_get_route_map_valid(self):
        response = self.client.get(reverse('get_route_map'), {'route': f"['{self.city1.name}', '{self.city2.name}', '{self.city3.name}']"})
        self.assertEqual(response.status_code, 200)

    # Test route map by passing cities that do not exist - ensure that it 404s
    def test_get_route_map_invalid_1(self):
        response = self.client.get(reverse('get_route_map'), {'route': "['Paris', 'Madrid', 'Lisbon']"})
        self.assertEqual(response.status_code, 404)

    # Test route map by passing cities that do not have routes between them - ensure that it 404s
    def test_get_route_map_invalid_2(self):
        response = self.client.get(reverse('get_route_map'), {'route': f"['{self.city1.name}', '{self.city3.name}', '{self.city4.name}']"})
        self.assertEqual(response.status_code, 404)
    
    # Test route map by ensuring that it returns a bad request when no parameters are passed
    def test_get_route_map_no_params(self):
        response = self.client.get(reverse('get_route_map'))
        self.assertEqual(response.status_code, 400)

    # Test full_map to ensure that it loads
    def test_full_map(self):
        response = self.client.get(reverse('full_map'))
        self.assertEqual(response.status_code, 200)

    # Test full_map to ensure that it loads
    def test_get_trip_map_valid(self):
        response = self.client.get(reverse('get_trip_map'), {'trip_id': 1})
        self.assertEqual(response.status_code, 200)

    # Test full_map to ensure that it loads
    def test_get_trip_map_invalid(self):
        response = self.client.get(reverse('get_trip_map'), {'trip_id': 5})
        self.assertEqual(response.status_code, 404)

    # Test full_map to ensure that it loads
    def test_get_trip_map_no_params(self):
        response = self.client.get(reverse('get_trip_map'))
        self.assertEqual(response.status_code, 400)