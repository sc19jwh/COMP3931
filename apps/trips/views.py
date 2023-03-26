# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.db.models import Min, Max
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
# Other imports
import base64
import folium
import ast
from datetime import datetime, date, timedelta
import decimal
# Folder imports
from .models import *
from apps.flights.models import *
from apps.authentication.models import Profile
from apps.hotels.models import Hotel
from .utils.geofuncs import lat_long_distance, dijkstra, least_transfers

def home(request):
    countries = Country.objects.filter(is_interrail=True)
    cities = City.objects.all()
    airports = Airport.objects.all()
    context = {'title': 'Home', 'countries': countries, 'cities': cities, 'profile': Profile.objects.get(user=request.user), 'airports': airports}
    return render(request, 'index.html', context)

@login_required
def mytrips(request, username):
    if User.objects.get(username=username) != request.user:
        raise Http404
    if request.method == 'POST':
        # If POST adding trip
        if 'add_trip_form' in request.POST:
            trip = Trip.objects.create(
                user=request.user,
                title=request.POST.get('triptitle'),
                journey_times=decimal.Decimal(request.POST.get('journeytime')),
                budget=decimal.Decimal(request.POST.get('budget')),
                climate=decimal.Decimal(request.POST.get('climate')),
                food_culture=decimal.Decimal(request.POST.get('food')),
                tourist_attractions=decimal.Decimal(request.POST.get('tourism')),
                nightlife_level=decimal.Decimal(request.POST.get('nightlife'))
            )
        # If POST deleting trip
        elif 'delete_trip_form' in request.POST:
            trip = get_object_or_404(Trip, id=request.POST.get('delete_trip_form'))
            trip.delete()
    trips = Trip.objects.filter(user=request.user)
    for trip in trips:
        trip.start_date = trip.destination_set.aggregate(Min('start_date'))['start_date__min']
        trip.end_date = trip.destination_set.aggregate(Max('end_date'))['end_date__max']
    context = {'title': 'My Trips', 'profile': Profile.objects.get(user=request.user), 'trips': trips}
    return render(request, 'mytrips.html', context)

@login_required
def configtrip(request, trip_id, username):
    trip = get_object_or_404(Trip, id=trip_id)
    if User.objects.get(username=username) != request.user:
        raise Http404
    if request.method == 'POST':
        # If POST adding destination
        if 'add_destination_form' in request.POST:
            destination = Destination.objects.create(
                trip=get_object_or_404(Trip, id=trip_id),
                country=get_object_or_404(Country, id=request.POST.get('country')),
                city=get_object_or_404(City, id=request.POST.get('city')),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date')
            )
        # If POST deleting destination
        elif 'delete_destination_form' in request.POST:
            destination = get_object_or_404(Destination, id=request.POST.get('delete_destination_form'))
            # If the first destination of trip is being deleted, delete any configured outbound flight
            if destination.id == trip.destination_set.order_by('start_date').first().id:
                Flight.objects.filter(trip_id=trip.id, direction='outbound').delete()
            # If the last destination of trip is being deleted, delete any configured inbound flight
            if destination.id == trip.destination_set.order_by('end_date').last().id:
                Flight.objects.filter(trip_id=trip.id, direction='inbound').delete()
            destination.delete()
        # If POST adding flights
        elif 'enter_flight_form' in request.POST:
            flight_direction = request.POST.get('enter_flight_form')
            departure_airport = request.POST.get('departure_airport')
            destination_airport = request.POST.get('destination_airport') 
            departure_datetime = datetime.strptime(request.POST.get('departure_datetime'), '%Y-%m-%dT%H:%M')
            destination_datetime = datetime.strptime(request.POST.get('destination_datetime'), '%Y-%m-%dT%H:%M')
            master_flight = Flight.objects.create(
                direction = flight_direction,
                trip = get_object_or_404(Trip, id=trip_id),
                departure_airport = get_object_or_404(Airport, id=departure_airport),
                arrival_airport = get_object_or_404(Airport, id=destination_airport),
                departure_datetime = departure_datetime,
                arrival_datetime = destination_datetime,
                duration = int((destination_datetime - departure_datetime).total_seconds() / 60),
                number_connections = int(request.POST.get('stops'))
            )
            master_flight.save()
        elif 'save_searched_flight' in request.POST:
            flight_details_dict = eval(dict(request.POST)['save_searched_flight'][0])
            if 'sub_flights' in flight_details_dict:
                num_stops = len(flight_details_dict['sub_flights'])
            else:
                num_stops = 0
            flight_direction = request.GET.get('flight_direction')
            departure_airport = get_object_or_404(Airport, id = request.GET.get('departure_airport'))
            destination_airport = get_object_or_404(Airport, id = request.GET.get('destination_airport'))
            departure_datetime = datetime.strptime(flight_details_dict['departure_time'], '%Y-%m-%d %H:%M:%S')
            destination_datetime = datetime.strptime(flight_details_dict['arrival_time'], '%Y-%m-%d %H:%M:%S')
            master_flight = Flight.objects.create(
                direction = flight_direction,
                trip = get_object_or_404(Trip, id=trip_id),
                departure_airport = departure_airport,
                arrival_airport = destination_airport,
                departure_datetime = departure_datetime,
                arrival_datetime = destination_datetime,
                duration = int((destination_datetime - departure_datetime).total_seconds() / 60),
                number_connections = num_stops - 1
            )
        elif 'save_searched_hotel' in request.POST:
            destination = get_object_or_404(Destination, id = request.GET.get('destination_id'))
            hotel_details_dict = eval(dict(request.POST)['save_searched_hotel'][0])
            hotel = Hotel.objects.create(
                destination = destination,
                name = hotel_details_dict['name'],
                hotel_url = hotel_details_dict['url'].split('?', 1)[0],
                latitude = hotel_details_dict['position']['latitude'],
                longitude = hotel_details_dict['position']['longitude'],
                star_rating = hotel_details_dict['numberOfStars'],
                custom_rating = hotel_details_dict['reviews']['reviewSummaryScore']
            )
            hotel.set_images(hotel_details_dict['images'])
            hotel.save()
        elif 'add_travel_form' in request.POST:
            route = request.POST['route_selection']
            # Convert route to an array using ast (get params are always string, even though formatted [a,b,c])
            route_array = ast.literal_eval(route)
            # Create a master DestinationTransport object between the two destinations
            destination_transport = DestinationTransport.objects.create(
                departure_destination=get_object_or_404(Destination, id=request.POST['start_id']),
                arrival_destination=get_object_or_404(Destination, id=request.POST['end_id'])
            )
            # Create sub TransportLegs for each journey between the two destinations
            for i in range(len(route_array)-1):
                start_city = get_object_or_404(City, name=route_array[i])
                end_city = get_object_or_404(City, name=route_array[i+1])
                route = get_object_or_404(TravelRoute, start_city=start_city, end_city=end_city)
                transport_leg = TransportLeg.objects.create(
                    trip_transport = destination_transport,
                    route = route
                )
                # Attach sub journey to master journey
                destination_transport.transport_legs.add(transport_leg)
    countries = Country.objects.all()
    outbound_flight = Flight.objects.filter(trip=trip, direction="outbound").first()
    inbound_flight = Flight.objects.filter(trip=trip, direction="inbound").first()
    destinations = trip.destination_set.order_by('start_date', 'end_date')
    context = {'title': 'My Trips', 'trip': trip, 'destinations': destinations, 'countries': countries, 'profile': Profile.objects.get(user=request.user), 'outbound_flight': outbound_flight,
               'inbound_flight': inbound_flight, 'current_date': date.today(), 'first_destination': trip.destination_set.order_by('start_date').first(),
               'last_destination': trip.destination_set.order_by('start_date').last()}
    return render(request, 'configtrip.html', context)

def find_cities(request):
    country = request.GET.get('country')
    cities = City.objects.filter(country=country)
    context = {'cities': cities}
    return render(request, 'partials/find_cities.html', context)

def dependent_dates(request):
    context = {'start_date': request.GET.get('start_date')}
    return render(request, 'partials/dependent_dates.html', context)

def add_trip(request):
    context = {}
    return render(request, 'partials/add_trip.html', context)

def add_destination(request):
    trip = Trip.objects.get(id=request.GET.get('trip'))
    # If there is more than 1 destination already configured, set min start date as end date of prior destination
    if len(trip.destination_set.all()) > 0:
        last_destination_date = trip.destination_set.order_by('start_date').last().end_date
        min_date = str(last_destination_date)
    # If this is the first destination, set min start date to tomorrow
    else:
        min_date = str(date.today() + timedelta(days=1))
    countries = Country.objects.filter(is_interrail=True)
    context = {'countries': countries, 'min_date': min_date}
    return render(request, 'partials/add_destination.html', context)

def add_travel(request):
    if request.method == "GET":
        # Get city object of both start and end city
        start_dest = get_object_or_404(Destination, id = request.GET.get('start'))
        end_dest = get_object_or_404(Destination, id = request.GET.get('end'))
        # Check if direct route exists between two cities
        try:
            direct_route = TravelRoute.objects.get(start_city = start_dest.city, end_city = end_dest.city)
            shortest_array = [start_dest.city.name, end_dest.city.name]
            least_array = [start_dest.city.name, end_dest.city.name]
        # If no direct route, using dijkstra to calculate the shortest and least connecting routes
        except TravelRoute.DoesNotExist:
            # Calculate two routes between the city, shortest and least connections
            shortest_array = dijkstra(City.objects.all(), TravelRoute.objects.all(), start_dest.city.name, end_dest.city.name)
            least_array = least_transfers(City.objects.all(), TravelRoute.objects.all(), start_dest.city.name, end_dest.city.name)
        context = {'start': request.GET.get('start'), 'end': request.GET.get('end'), 'start_dest': start_dest, 'end_dest': end_dest,
                'shortest': shortest_array, 'least': least_array}
        return render(request, 'partials/add_travel.html', context)
        return HttpResponse(status=200)