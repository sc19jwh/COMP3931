from django.shortcuts import render
from .utils.flights import quick_flight_search, full_flight_search

def add_flight(request):
    flight_direction = request.GET.get('flight_direction')
    print(flight_direction)
    context = {'flight_direction': flight_direction}
    return render(request, 'partials/add_flight.html', context)

def enter_flight(request):
    flight_direction = request.GET.get('flight_direction')
    print(flight_direction)
    context = {}
    return render(request, 'partials/enter_flight.html', context)

def search_flight(request):
    context = {}
    return render(request, 'partials/search_flight.html', context)

def search_results(request):
    session_token, direct_flights, connecting_flights = quick_flight_search("GBP", "MAN", "NAP", 2023, 6, 12, True)
    if request.method == "POST":
        direct_flights, connecting_flights = full_flight_search(session_token, False)
    context = {'direct_flights': direct_flights, 'connecting_flights': connecting_flights}
    return render(request, 'partials/search_results.html', context)
