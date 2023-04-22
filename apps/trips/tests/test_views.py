from django.test import TestCase, Client
from django.urls import resolve, reverse
from apps.trips.views import *
from apps.trips.models import Country
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
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.profile = Profile.objects.create(user=self.user, nationality=self.country)
        # Create a trip object
        self.trip = Trip.objects.create(
            user=self.user,
            title='Unit Test Trip',
            start_date='2024-03-01',
            journey_times=50,
            climate=50
        )
        # Create a second user account
        self.alt_username = 'alternativeuser'
        self.alt_password = 'alternativepassword'
        self.alt_user = User.objects.create_user(username=self.alt_username, password=self.alt_password)
        self.alt_profile = Profile.objects.create(user=self.alt_user, nationality=self.country)

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
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.profile = Profile.objects.create(user=self.user, nationality=self.country)
        self.client.login(username=self.username, password=self.password)

    def test_add_trip(self):
        # POST data
        response = self.client.post(reverse('mytrips', args=[self.username]), {'add_trip_form': 'add_trip',
            'triptitle': 'Unit Test Trip',
            'start_date': '2024-03-01',
            'journeytime': '50.1',
            'climate': '35',
            'food_budget': '30.7',
            'accom_budget': '15.5'
        })
        # Get newly created trip
        trip = Trip.objects.get(user=self.user, title='Unit Test Trip')
        # Check that model exactly matches inputted data
        self.assertEqual(trip.start_date, datetime.strptime('2024-03-01', '%Y-%m-%d').date())
        self.assertEqual(trip.journey_times, Decimal('50.1'))
        self.assertEqual(trip.climate, Decimal('35'))
        self.assertEqual(trip.food_budget, Decimal('30.7'))
        self.assertEqual(trip.accom_budget, Decimal('15.5'))

    def test_delete_trip(self):
        # Temporarily create a Trip object
        trip = Trip.objects.create(
            user=self.user,
            title='Unit Test Trip',
            start_date='2024-03-01',
            journey_times=50.1,
            climate=35
        )
        # POST the data
        response = self.client.post(reverse('mytrips', args=[self.username]), {'delete_trip_form': trip.id})
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
        # Add destination to trip
        self.destination1 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city1, order = 1, nights = 1)

    # Test valid request to config trip page
    def test_configtrip_valid(self):
        response = self.client.post(reverse('configtrip', args=[self.username, self.trip.id]))
        self.assertEqual(response.status_code, 200)

    # Test invalid request to config trip page
    def test_configtrip_invalid(self):
        response = self.client.post(reverse('configtrip', args=[self.username, 100]))
        self.assertEqual(response.status_code, 404)

    # Test edit to valid trip
    def test_edit_trip_details_valid(self):
        response = self.client.post(reverse('configtrip', args=[self.username, self.trip.id]),
            {'edit_trip_details_form': '',
            'triptitle': 'New Title',
            'start_date': '2024-01-01'}
        )
        self.updated_trip = Trip.objects.get(id = self.trip.id)
        self.assertEqual(self.updated_trip.title, 'New Title')
        self.assertEqual(str(self.updated_trip.start_date), '2024-01-01')
        with self.assertRaises(Flight.DoesNotExist):
            Flight.objects.get(id=self.flight.id)

    # Testing adding a valid destination to the end of current itinerary
    def test_add_destination_valid(self):
        response = self.client.post(reverse('configtrip', args=[self.username, self.trip.id]),
            {'add_destination_form': '',
            'next_order': '2',
            'country': self.country.id,
            'city': self.city2.id,
            'nights': '1'}
        )
        created = Destination.objects.get(trip=self.trip, city=self.city2)
        self.assertEqual(created.order, 2)
        self.assertEqual(created.nights, 1)

    # Test adding a new trip in the middle of existing itinerary (ensure existing order is shifted up correctly)
    def test_add_destination_valid_2(self):
        response = self.client.post(reverse('configtrip', args=[self.username, self.trip.id]),
            {'add_destination_form': '',
            'next_order': '1',
            'country': self.country.id,
            'city': self.city2.id,
            'nights': '1'}
        )
        created = Destination.objects.get(trip=self.trip, city=self.city2)
        self.assertEqual(created.order, 1)
        self.assertEqual(created.nights, 1)
        old = Destination.objects.get(id = self.destination1.id)
        self.assertEqual(old.order, 2)

    # Test editing a trip by modifying the number of nights - assert that the change was made successfully
    def test_edit_destination_valid(self):
        response = self.client.post(reverse('configtrip', args=[self.username, self.trip.id]),
            {'edit_destination_form': self.destination1.id,
            'new_nights': '5',}
        )
        updated_destination = Destination.objects.get(id = self.destination1.id)
        self.assertEqual(updated_destination.nights, 5)

    # Test editing a destination with an invalid destination id - should 404
    def test_edit_destination_invalid(self):
        response = self.client.post(reverse('configtrip', args=[self.username, self.trip.id]),
            {'edit_destination_form': 100,
            'new_nights': '1',}
        )
        self.assertEqual(response.status_code, 404)

    # Test deleting a destination - check that the destination is deleted as well as the outbound and inbound flights
    def test_delete_destination_valid(self):
        response = self.client.post(reverse('configtrip', args=[self.username, self.trip.id]),
            {'delete_destination_form': self.destination1.id}
        )
        with self.assertRaises(Destination.DoesNotExist):
            Destination.objects.get(id=self.destination1.id)
        with self.assertRaises(Flight.DoesNotExist):
            Flight.objects.get(id=self.flight.id)
        with self.assertRaises(Flight.DoesNotExist):
            Flight.objects.get(id=self.flight2.id)

    # Test deleting a destination with an invalid destination id - should 404
    def test_delete_destination_invalid(self):
        response = self.client.post(reverse('configtrip', args=[self.username, self.trip.id]),
            {'delete_destination_form': 1000}
        )   
        self.assertEqual(response.status_code, 404) 

    # Test entering a valid flight using form
    def test_enter_flight_valid(self):
        delete = Flight.objects.get(id = self.flight.id).delete()
        response = self.client.post(reverse('configtrip', args=[self.username, self.trip.id]),
            {'enter_flight_form': 'outbound',
             'departure_airport': self.airport1.id,
             'destination_airport': self.airport2.id,
             'departure_datetime': '2024-01-01T12:00',
             'destination_datetime': '2024-01-01T14:00', 
             'stops': '0'}
        )
        created_flight = Flight.objects.get(trip = self.trip, direction = 'outbound')
        self.assertEqual(created_flight.departure_airport, self.airport1)
        self.assertEqual(created_flight.arrival_airport, self.airport2)
        self.assertEqual(created_flight.duration, 120)
        self.assertEqual(str(created_flight.departure_datetime), "2024-01-01 12:00:00")
        self.assertEqual(str(created_flight.arrival_datetime), "2024-01-01 14:00:00")
        self.assertEqual(created_flight.number_connections, 0)

    # Test adding travel between two destinations
    def test_add_travel_valid(self):
        self.destination2 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city2, order = 2, nights = 1)
        self.route_array = str([self.destination1.city.name, self.destination2.city.name])
        response = self.client.post(reverse('configtrip', args=[self.username, self.trip.id]),
            {'add_travel_form': '',
             'route_selection': self.route_array,
             'start_id': self.destination1.id,
             'end_id': self.destination2.id}
        )
        created_destination_transport = DestinationTransport.objects.get(departure_destination = self.destination1, arrival_destination = self.destination2)
        created_transport_leg = TransportLeg.objects.get(route = self.travel_route, trip_transport = created_destination_transport)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(created_destination_transport.departure_destination, self.destination1)
        self.assertEqual(created_destination_transport.arrival_destination, self.destination2)
        self.assertEqual(created_transport_leg.route, self.travel_route)

    # Testing editing travel between two destinations
    def test_edit_travel_valid(self):
        self.destination2 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city2, order = 2, nights = 1)
        self.route_array = str([self.destination1.city.name, self.destination2.city.name])
        response = self.client.post(reverse('configtrip', args=[self.username, self.trip.id]),
            {'edit_travel_form': '',
             'route_selection': self.route_array,
             'start_id': self.destination1.id,
             'end_id': self.destination2.id}
        )
        created_destination_transport = DestinationTransport.objects.get(departure_destination = self.destination1, arrival_destination = self.destination2)
        created_transport_leg = TransportLeg.objects.get(route = self.travel_route, trip_transport = created_destination_transport)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(created_destination_transport.departure_destination, self.destination1)
        self.assertEqual(created_destination_transport.arrival_destination, self.destination2)
        self.assertEqual(created_transport_leg.route, self.travel_route)

    # Test deleting a trip's flight (outbound and inbound)
    def test_delete_flight_form_valid(self):
        response = self.client.post(reverse('configtrip', args=[self.username, self.trip.id]),
            {'delete_flight_form': 'outbound'}
        )
        with self.assertRaises(Flight.DoesNotExist):
            Flight.objects.get(id=self.flight.id)
        response = self.client.post(reverse('configtrip', args=[self.username, self.trip.id]),
            {'delete_flight_form': 'inbound'}
        )
        with self.assertRaises(Flight.DoesNotExist):
            Flight.objects.get(id=self.flight2.id)

class FindCitiesFunctionalityTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.city1 = City.objects.create(name="London", country=self.country)
        self.city2 = City.objects.create(name="Bristol", country=self.country)
        self.city3 = City.objects.create(name="Birmingham", country=self.country)
        self.client = Client()
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_find_cities(self):
        response = self.client.get(reverse('find_cities'), {'country': self.country.id})
        self.assertContains(response, self.city1.name)
        self.assertContains(response, self.city2.name)
        self.assertContains(response, self.city3.name)

class AddTripFunctionalityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_add_trip(self):
        response = self.client.get(reverse('add_trip'))
        self.assertEqual(response.status_code, 200)

class AddDestinationFunctionalityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.trip = Trip.objects.create(user = self.user, title = "Test Trip")

    def test_add_destination(self):
        response = self.client.get(reverse('add_destination'), {'trip': self.trip.id, 'next_order': 1})
        self.assertEqual(response.status_code, 200)

class AddTravelFunctionalityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.trip = Trip.objects.create(user = self.user, title = "Test Trip")
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.city1 = City.objects.create(name="London", country=self.country)
        self.city2 = City.objects.create(name="Bristol", country=self.country)
        self.start_dest = Destination.objects.create(trip = self.trip, country = self.country, city = self.city1, order = 1, nights = 1)
        self.end_dest = Destination.objects.create(trip = self.trip, country = self.country, city = self.city2, order = 2, nights = 2)
        self.travel_route = TravelRoute.objects.create(start_city = self.city1, end_city = self.city2, duration = 100, type = "train")

    def test_add_travel(self):
        response = self.client.get(reverse('add_travel'), {'start': self.start_dest.id, 'end': self.end_dest.id})
        self.assertEqual(response.status_code, 200)

class TripSummaryFunctionalityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.trip = Trip.objects.create(user = self.user, title = "Test Trip")
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.city1 = City.objects.create(name="London", country=self.country)
        self.city2 = City.objects.create(name="Bristol", country=self.country)
        self.dest1 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city1, order = 1, nights = 1)
        self.dest2 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city2, order = 2, nights = 2)
        self.travel_route = TravelRoute.objects.create(start_city = self.city1, end_city = self.city2, duration = 100, type = "train")
        self.destination_transport = DestinationTransport.objects.create(departure_destination = self.dest1, arrival_destination = self.dest2)
        self.leg = TransportLeg.objects.create(trip_transport = self.destination_transport, route = self.travel_route)

    def test_trip_summary(self):
        response = self.client.get(reverse('trip_summary'), {'trip_id': self.trip.id})
        self.assertContains(response, self.city1.name)
        self.assertContains(response, self.city2.name)
        self.assertEqual(response.status_code, 200)

class JourneySummaryFunctionalityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.trip = Trip.objects.create(user = self.user, title = "Test Trip")
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.city1 = City.objects.create(name="London", country=self.country)
        self.city2 = City.objects.create(name="Bristol", country=self.country)
        self.dest1 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city1, order = 1, nights = 1)
        self.dest2 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city2, order = 2, nights = 2)
        self.travel_route = TravelRoute.objects.create(start_city = self.city1, end_city = self.city2, duration = 100, type = "train")
        self.destination_transport = DestinationTransport.objects.create(departure_destination = self.dest1, arrival_destination = self.dest2)
        self.leg = TransportLeg.objects.create(trip_transport = self.destination_transport, route = self.travel_route)
        self.route_array = str([self.city1.name, self.city2.name])

    def test_journey_summary(self):
        response = self.client.get(reverse('journey_summary'), {'route': self.route_array})
        self.assertContains(response, self.city1.name)
        self.assertContains(response, self.city2.name)
        self.assertEqual(response.status_code, 200)

class EditDestinationFunctionalityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.trip = Trip.objects.create(user = self.user, title = "Test Trip")
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.city1 = City.objects.create(name="London", country=self.country)
        self.dest1 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city1, order = 1, nights = 1)

    def test_edit_destination_valid(self):
        response = self.client.get(reverse('edit_destination'), {'destination_id': self.dest1.id, 'nights': 2})
        self.assertEqual(response.status_code, 200)

    def test_edit_destination_invalid(self):
        response = self.client.get(reverse('edit_destination'), {'destination_id': 100, 'nights': 2})
        self.assertEqual(response.status_code, 404)

class EditTripDetailsFunctionalityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.trip = Trip.objects.create(user = self.user, title = "Test Trip")
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.city1 = City.objects.create(name="London", country=self.country)
        self.dest1 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city1, order = 1, nights = 1)

    def test_edit_trip_details_valid(self):
        response = self.client.get(reverse('edit_trip_details'), {'trip_id': self.trip.id})
        self.assertEqual(response.status_code, 200)

    def test_edit_trip_details_invalid(self):
        response = self.client.get(reverse('edit_trip_details'), {'trip_id': 100})
        self.assertEqual(response.status_code, 404)

class EditTravelFunctionalityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.trip = Trip.objects.create(user = self.user, title = "Test Trip")
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.city1 = City.objects.create(name="London", country=self.country)
        self.city2 = City.objects.create(name="Birmingham", country=self.country)
        self.dest1 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city1, order = 1, nights = 2)
        self.dest2 = Destination.objects.create(trip = self.trip, country = self.country, city = self.city2, order = 2, nights = 3)
        self.travel_route = TravelRoute.objects.create(start_city = self.city1, end_city = self.city2, duration = 100, type = "train")
        self.destination_transport = DestinationTransport.objects.create(departure_destination = self.dest1, arrival_destination = self.dest2)
        self.leg = TransportLeg.objects.create(trip_transport = self.destination_transport, route = self.travel_route)

    def test_edit_trip_details_valid(self):
        response = self.client.get(reverse('edit_travel'), {'start': self.dest1.id, 'end': self.dest2.id})
        self.assertEqual(response.status_code, 200)

    def test_edit_trip_details_invalid(self):
        response = self.client.get(reverse('edit_travel'), {'start': 100, 'end': 1002})
        self.assertEqual(response.status_code, 404)