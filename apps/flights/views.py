# Django imports
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
# Folder imports
from .utils.sky import quick_flight_search
from .models import *
from apps.trips.models import *

def add_flight(request):
    flight_direction = request.GET.get('flight_direction')
    trip_id = request.GET.get('trip_id')
    context = {'flight_direction': flight_direction, 'trip_id': trip_id}
    return render(request, 'partials/add_flight.html', context)

def enter_flight(request):
    trip_id = request.GET.get('trip_id')
    flight_direction = request.GET.get('flight_direction')
    trip = get_object_or_404(Trip, id=trip_id)
    if flight_direction == "outbound":
        earliest_destination = trip.destination_set.order_by('order').first()
        departure_airports = Airport.objects.all()
        arrival_interrailairports = InterrailAirport.objects.filter(city=earliest_destination.city)
        # Get arrival airports as Airport objects
        arrival_airports = []
        for airport in arrival_interrailairports:
            arrival_airports.append(airport.airport)
    else:
        last_destination = trip.destination_set.order_by('order').last()
        departure_interrailairports = InterrailAirport.objects.filter(city=last_destination.city)
        # Get departure airports as Airport objects
        departure_airports = []
        for airport in departure_interrailairports:
            departure_airports.append(airport.airport)
        arrival_airports = Airport.objects.all()
    context = {'popup_title': 'Enter Flight', 'departure_airports': departure_airports, 'arrival_airports': arrival_airports, 'flight_direction': flight_direction}
    return render(request, 'partials/enter_flight.html', context)

def search_flight(request):
    # Get trip and flight direction from get request
    trip = get_object_or_404(Trip, id=request.GET.get('trip_id'))
    flight_direction = request.GET.get('flight_direction')
    # If outbound flight, find the earliest destination's start date and find a flight to that destination on that date
    if flight_direction == "outbound":
        earliest_destination = trip.destination_set.order_by('order').first()
        departure_airports = Airport.objects.all()
        arrival_interrailairports = InterrailAirport.objects.filter(city=earliest_destination.city)
        # Get arrival airports as Airport objects
        arrival_airports = []
        for airport in arrival_interrailairports:
            arrival_airports.append(airport.airport)
    # If inbound flight, find the last destination's end date and find a flight from that destination on that date
    else:
        last_destination = trip.destination_set.order_by('order').last()
        departure_interrailairports = InterrailAirport.objects.filter(city=last_destination.city)
        # Get departure airports as Airport objects
        departure_airports = []
        for airport in departure_interrailairports:
            departure_airports.append(airport.airport)
        arrival_airports = Airport.objects.all()
    context = {'popup_title': 'Flight Search', 'departure_airports': departure_airports, 'arrival_airports': arrival_airports, 'trip_id': trip.id, 'flight_direction': flight_direction}
    return render(request, 'partials/search_flight.html', context)

def search_results(request):
    # Get trip id, direction and direct flights flag from parameters
    trip = get_object_or_404(Trip, id=request.GET.get('trip_id'))
    flight_direction = request.GET.get('flight_direction')
    if request.GET.get('direct_flights') == 'on':
        direct = True
    else:
        direct = False
    # Get airport objects from IDs
    departure_airport = get_object_or_404(Airport, id = request.GET.get('departure_airport'))
    destination_airport = get_object_or_404(Airport, id = request.GET.get('arrival_airport'))
    # If outbound flight configure dates as trip start date
    if flight_direction == "outbound":
        earliest_destination = trip.destination_set.order_by('order').first()
        session_token, direct_flights, connecting_flights = quick_flight_search("GBP", departure_airport.iata_code, destination_airport.iata_code, earliest_destination.start_date.year, earliest_destination.start_date.month, earliest_destination.start_date.day, direct)
    # If inbound flight configure dates as trip end date
    else:
        last_destination = trip.destination_set.order_by('order').last()
        session_token, direct_flights, connecting_flights = quick_flight_search("GBP", departure_airport.iata_code, destination_airport.iata_code, last_destination.start_date.year, last_destination.start_date.month, last_destination.start_date.day, direct)
    context = {'direct_flights': direct_flights, 'connecting_flights': connecting_flights, 'flight_direction': flight_direction, 'departure_airport': departure_airport, 'destination_airport': destination_airport}
    return render(request, 'partials/search_results.html', context)

def airport_search(request):
    airports = []
    if request.method == "POST":
        search_term = request.POST.get('search')
        if len(search_term) > 0:
            airports = Airport.objects.filter(
                Q(name__icontains=search_term) | 
                Q(country__name__icontains=search_term) |
                Q(iata_code__icontains=search_term)
            )[:3]
    context = {'airports': airports}
    return render(request, 'partials/airport_search.html', context)