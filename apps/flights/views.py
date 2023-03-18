# Django imports
from django.shortcuts import render, get_object_or_404
# Folder imports
from .utils.flights import quick_flight_search, full_flight_search
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
        # If outbound flight, find the earliest destination's start date and find a flight to that destination on that date
        earliest_destination = trip.destination_set.order_by('start_date').first()
        chosen_airports = earliest_destination.city.airport_set.all()
    else:
        # If inbound flight, find the last destination's end date and find a flight from that destination on that date
        last_destination = trip.destination_set.order_by('end_date').last()
        chosen_airports = last_destination.city.airport_set.all()
    context = {'airports': Airport.objects.all(), 'chosen_airports': chosen_airports, 'flight_direction': flight_direction}
    return render(request, 'partials/enter_flight.html', context)

def search_results(request):
    # Get trip id and direction from parameters
    trip_id = request.GET.get('trip_id')
    flight_direction = request.GET.get('flight_direction')
    # Get trip object from trip id
    trip = get_object_or_404(Trip, id=trip_id)
    # If outbound flight get first destination date and vice versa for inbound flight
    if flight_direction == "outbound":
        # If outbound flight, find the earliest destination's start date and find a flight to that destination on that date
        earliest_destination = trip.destination_set.order_by('start_date').first()
        destination_airport = earliest_destination.city.airport_set.first()
        print("GBP", "LHR", destination_airport.iata_code, earliest_destination.start_date.year, earliest_destination.start_date.month, earliest_destination.start_date.day, False)
        session_token, direct_flights, connecting_flights = quick_flight_search("GBP", "LHR", destination_airport.iata_code, earliest_destination.start_date.year, earliest_destination.start_date.month, earliest_destination.start_date.day, False)
    else:
        # If inbound flight, find the last destination's end date and find a flight from that destination on that date
        last_destination = trip.destination_set.order_by('end_date').last()
        departure_airport = last_destination.city.airport_set.last()
        session_token, direct_flights, connecting_flights = quick_flight_search("GBP", departure_airport.iata_code, "LHR", last_destination.end_date.year, last_destination.end_date.month, last_destination.end_date.day, False)
    context = {'direct_flights': direct_flights, 'connecting_flights': connecting_flights}
    return render(request, 'partials/search_results.html', context)
