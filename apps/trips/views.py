# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.db.models import Min, Max, Q
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
    # airports = Airport.objects.all()
    if request.method == 'POST':
        # print(request.POST)
        print(request.POST.get('test'))
    context = {'title': 'Home', 'countries': countries, 'cities': cities, 'profile': Profile.objects.get(user=request.user)}
    return render(request, 'index.html', context)

@login_required
def mytrips(request, username):
    if User.objects.get(username=username) != request.user:
        return HttpResponse(status=401)
    if request.method == 'POST':
        # If POST adding trip
        if 'add_trip_form' in request.POST:
            trip = Trip.objects.create(
                user=request.user,
                title=request.POST.get('triptitle'),
                start_date=request.POST.get('start_date'),
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
    if len(trips) == 0:
        middle = True
    else:
        middle = False
    context = {'title': 'My Trips', 'profile': Profile.objects.get(user=request.user), 'trips': trips, 'middle': middle}
    return render(request, 'mytrips.html', context)

@login_required
def configtrip(request, trip_id, username):
    trip = get_object_or_404(Trip, id=trip_id)
    if User.objects.get(username=username) != request.user:
        return HttpResponse(status=401)
    if request.method == 'POST':
        if 'edit_trip_details_form' in request.POST:
            new_title = request.POST.get('triptitle')
            new_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
            # If title is modified, write the change
            if new_title != trip.title:
                trip.title = new_title
                trip.save()
            # If date is modified, write the change
            if new_date != trip.start_date:
                trip.start_date = new_date
                trip.save()
                # If date changed remove any flights
                flights = Flight.objects.filter(trip_id=trip.id).delete()
        elif 'add_destination_form' in request.POST:
            order_to_add = int(request.POST.get('next_order'))
            # Only perform if destinations already exist on trip
            if trip.destination_set.count() > 1:
                # Look up order - if order is 1 remove any outbound flights and always remove inbound flight as adding any new destination will modify end date
                if order_to_add == 1:
                    Flight.objects.filter(trip_id=trip.id, direction='outbound').delete()
                else:
                    Flight.objects.filter(trip_id=trip.id, direction='inbound').delete()
                    # If adding a new destination between two configured destinations, delete any transport between them
                    start_dest = Destination.objects.get(trip = trip, order = order_to_add-1)
                    end_dest = Destination.objects.get(trip = trip, order = order_to_add)
                    DestinationTransport.objects.filter(departure_destination = start_dest, arrival_destination = end_dest).delete()
            # Get destinations equal to or greater than that order and push them up one spot
            adjust_orders = Destination.objects.filter(order__gte=order_to_add)
            for destination in adjust_orders:
                destination.order += 1
                destination.save()
            destination = Destination.objects.create(
                trip=get_object_or_404(Trip, id=trip_id),
                country=get_object_or_404(Country, id=request.POST.get('country')),
                city=get_object_or_404(City, id=request.POST.get('city')),
                order = order_to_add,
                nights = request.POST.get('nights')
            )
        elif 'edit_destination_form' in request.POST:
            # Get destination and modified number of nights
            destination = get_object_or_404(Destination, id=request.POST.get('edit_destination_form'))
            # Write new number of nights to destination
            destination.nights = int(request.POST.get('new_nights'))
            destination.save()
            # Delete any inbound flights that exist on trip as this effects end dates
            Flight.objects.filter(trip_id=destination.trip.id, direction='inbound').delete()
        # If POST deleting destination
        elif 'delete_destination_form' in request.POST:
            destination = get_object_or_404(Destination, id=request.POST.get('delete_destination_form'))
            # If the first destination of trip is being deleted, delete any configured outbound flight
            if destination.id == trip.destination_set.order_by('order').first().id:
                Flight.objects.filter(trip_id=trip.id, direction='outbound').delete()
            # If the last destination of trip is being deleted, delete any configured inbound flight
            if destination.id == trip.destination_set.order_by('order').last().id:
                Flight.objects.filter(trip_id=trip.id, direction='inbound').delete()
            destination.delete()
            # Get destinations greater than that order and push them down one spot
            adjust_orders = Destination.objects.filter(order__gt=destination.order)
            for destination in adjust_orders:
                destination.order -= 1
                destination.save()
        # If POST adding flights
        elif 'enter_flight_form' in request.POST:
            flight_direction = request.POST.get('enter_flight_form')
            departure_airport = request.POST.get('departure_airport')
            destination_airport = request.POST.get('destination_airport') 
            departure_datetime = datetime.strptime(request.POST.get('departure_datetime'), '%Y-%m-%dT%H:%M')
            destination_datetime = datetime.strptime(request.POST.get('destination_datetime'), '%Y-%m-%dT%H:%M')
            flight = Flight.objects.create(
                direction = flight_direction,
                trip = get_object_or_404(Trip, id=trip_id),
                departure_airport = get_object_or_404(Airport, id=departure_airport),
                arrival_airport = get_object_or_404(Airport, id=destination_airport),
                departure_datetime = departure_datetime,
                arrival_datetime = destination_datetime,
                duration = int((destination_datetime - departure_datetime).total_seconds() / 60),
                number_connections = int(request.POST.get('stops'))
            )
            flight.save()
        elif 'save_searched_flight' in request.POST:
            flight_details_dict = eval(dict(request.POST)['save_searched_flight'][0])
            if 'sub_flights' in flight_details_dict:
                num_stops = len(flight_details_dict['sub_flights']) - 1
            else:
                num_stops = 0
            flight_direction = request.GET.get('flight_direction')
            departure_airport = get_object_or_404(Airport, id = request.GET.get('departure_airport'))
            destination_airport = get_object_or_404(Airport, id = request.GET.get('destination_airport'))
            departure_datetime = datetime.strptime(flight_details_dict['departure_time'], '%Y-%m-%d %H:%M:%S')
            destination_datetime = datetime.strptime(flight_details_dict['arrival_time'], '%Y-%m-%d %H:%M:%S')
            flight = Flight.objects.create(
                direction = flight_direction,
                trip = get_object_or_404(Trip, id=trip_id),
                departure_airport = departure_airport,
                arrival_airport = destination_airport,
                departure_datetime = departure_datetime,
                arrival_datetime = destination_datetime,
                duration = flight_details_dict['duration'],
                number_connections = num_stops
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
    destinations = trip.destination_set.order_by('order')
    if len(destinations) == 0:
        middle = True
    else:
        middle = False
    context = {'title': 'My Trips', 'trip': trip, 'destinations': destinations, 'countries': countries, 'profile': Profile.objects.get(user=request.user), 'outbound_flight': outbound_flight,
               'inbound_flight': inbound_flight, 'current_date': date.today(), 'first_destination': trip.destination_set.order_by('order').first(),
               'last_destination': trip.destination_set.order_by('order').last(), 'middle': middle}
    return render(request, 'configtrip.html', context)

def find_cities(request):
    country = request.GET.get('country')
    cities = City.objects.filter(country=country)
    context = {'cities': cities}
    return render(request, 'partials/find_cities.html', context)

def add_trip(request):
    context = {'today': str(date.today() + timedelta(days=1)), 'popup_title': 'Create new trip'}
    return render(request, 'partials/add_trip.html', context)

def add_destination(request):
    trip = Trip.objects.get(id=request.GET.get('trip'))
    next_order = request.GET.get('next_order')
    countries = Country.objects.filter(is_interrail=True)
    # Check if any flights exist for trip - will control whether warning is needed or not
    inbound_flight = Flight.objects.filter(trip_id=trip.id, direction='inbound')
    context = {'countries': countries, 'next_order': next_order, 'inbound_flight': inbound_flight}
    return render(request, 'partials/add_destination.html', context)

def add_travel(request):
    # Get city object of both start and end city
    start_dest = get_object_or_404(Destination, id = request.GET.get('start'))
    end_dest = get_object_or_404(Destination, id = request.GET.get('end'))
    # Check if direct route exists between two cities
    try:
        direct_route = TravelRoute.objects.get(start_city = start_dest.city, end_city = end_dest.city)
        shortest_array = [start_dest.city.name, end_dest.city.name]
        least_array = [start_dest.city.name, end_dest.city.name]
        shortest_length_hours, shortest_length_mins = divmod(direct_route.duration, 60)
        least_length_hours, least_length_mins = divmod(direct_route.duration, 60)
    # If no direct route, using dijkstra to calculate the shortest and least connecting routes
    except TravelRoute.DoesNotExist:
        # Calculate two routes between the city, shortest and least connections
        shortest_array, shortest_length = dijkstra(City.objects.all(), TravelRoute.objects.all(), start_dest.city.name, end_dest.city.name)
        least_array, least_length = least_transfers(City.objects.all(), TravelRoute.objects.all(), start_dest.city.name, end_dest.city.name)
        # Convert to hours and minutes
        shortest_length_hours, shortest_length_mins = divmod(shortest_length, 60)
        least_length_hours, least_length_mins = divmod(least_length, 60)
    context = {'start': request.GET.get('start'), 'end': request.GET.get('end'), 'start_dest': start_dest, 'end_dest': end_dest,
            'shortest': shortest_array, 'least': least_array, 'popup_title': f'{start_dest.city.name} - {end_dest.city.name}',
            'shortest_length_hours': shortest_length_hours, 'shortest_length_mins': shortest_length_mins, 'least_length_hours': least_length_hours,
            'least_length_mins': least_length_mins}
    return render(request, 'partials/add_travel.html', context)
    return HttpResponse(status=200)

def trip_summary(request):
    trip = get_object_or_404(Trip, id = request.GET.get('trip_id'))
    context = {'trip': trip, 'popup_title': f"Trip Summary - {trip.title}"}
    return render(request, 'partials/trip_summary.html', context)

def journey_summary(request):
    route = eval(request.GET.get('route'))
    travel_routes = TravelRoute.objects.all()
    journey_times_hours = []
    journey_times_mins = []
    journey_types = []
    for i in range(0, len(route)-1):
        for travel_route in travel_routes:
            if travel_route.start_city.name == route[i] and travel_route.end_city.name == route[i + 1]:
                # Once found add to duration
                hours, mins = divmod(travel_route.duration, 60)
                journey_times_hours.append(hours)
                journey_times_mins.append(mins)
                journey_types.append(travel_route.type.capitalize())
    # Add an extra spacing element to the times and types arrays to make them the same length as the route array
    journey_times_hours.append(0)
    journey_times_mins.append(0)
    journey_types.append('N/A')
    # Combine together for looping in tepmlate
    journey_zip = zip(route, journey_times_hours, journey_times_mins, journey_types)
    context = {'popup_title': f"{route[i]} - {route[len(route)-1]}", 'route': journey_zip}
    return render(request, 'partials/journey_summary.html', context)

def edit_destination(request):
    destination = get_object_or_404(Destination, id = request.GET.get('destination_id'))
    nights = int(request.GET.get('nights'))
    # Check if any flights exist for trip - will control whether warning is needed or not
    inbound_flight = Flight.objects.filter(trip_id=destination.trip.id, direction='inbound')
    context = {'popup_title': 'Edit Destination', 'destination': destination, 'nights': nights,
               'inbound_flight': inbound_flight}
    return render(request, 'partials/edit_destination.html', context)

def edit_trip_details(request):
    trip = get_object_or_404(Trip, id = request.GET.get('trip_id'))
    # Check if any flights exist for trip - will control whether warning is needed or not
    flights = Flight.objects.filter(trip_id=trip.id)
    context = {'popup_title': 'Edit Trip Details', 'trip': trip, 'flights': flights,
               'tomorrow': str(date.today() + timedelta(days=1))}
    return render(request, 'partials/edit_trip_details.html', context)