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
# Folder imports
from .models import *
from apps.authentication.models import Profile
from .utils.geofuncs import lat_long_distance, dijkstra, least_transfers

def home(request):
    countries = Country.objects.filter(is_interrail=True)
    cities = City.objects.all()
    context = {'title': 'Home', 'countries': countries, 'cities': cities}
    return render(request, 'index.html', context)

@login_required
def mytrips(request, username):
    if User.objects.get(username=username) != request.user:
        raise Http404
    if request.method == 'POST':
        # If POST adding trip
        if 'add_trip_form' in request.POST:
            trip = Trip.objects.create(
                user = request.user,
                title = request.POST.get('title')
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
            destination.delete()
    countries = Country.objects.all()
    trip = get_object_or_404(Trip, id=trip_id)
    destinations = trip.destination_set.order_by('start_date', 'end_date')
    context = {'title': 'My Trips', 'trip': trip, 'destinations': destinations, 'countries': countries, 'profile': Profile.objects.get(user=request.user)}
    return render(request, 'configtrip.html', context)

def find_cities(request):
    country = request.GET.get('country')
    cities = City.objects.filter(country=country)
    context = {'cities': cities}
    return render(request, 'partials/find_cities.html', context)

def dependent_dates(request):
    start_date = request.GET.get('start_date')
    context = {'start_date': start_date}
    return render(request, 'partials/dependent_dates.html', context)

def add_trip(request):
    context = {}
    return render(request, 'partials/add_trip.html', context)

def add_destination(request):
    countries = Country.objects.filter(is_interrail=True)
    context = {'countries': countries}
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
    elif request.method == "POST":
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
        return HttpResponse(status=200)

def get_travel_map(request):
    # Get the start and end point destination IDs
    start = get_object_or_404(Destination, id=request.GET.get('start'))
    end = get_object_or_404(Destination, id=request.GET.get('end'))
    # Use custom formula and distance to calculate a custom zoom level
    zoom = 6 - (lat_long_distance(start.city.latitude, start.city.longitude, end.city.latitude, end.city.longitude) / 500)
    # Create a map, with latitude and longitude centered around the two locations
    map = folium.Map(location=[(start.city.latitude + end.city.latitude) / 2, (start.city.longitude + end.city.longitude) / 2], zoom_start=zoom)
    # Add both locations and a line between the two
    folium.Marker(location=[start.city.latitude, start.city.longitude], popup=start.city.name, icon=folium.Icon(color='orange', icon='location-pin', prefix='fa'), tooltip=start.city.name,).add_to(map)
    folium.Marker(location=[end.city.latitude, end.city.longitude], popup=end.city.name, icon=folium.Icon(color='orange', icon='flag-checkered', prefix='fa'), tooltip=end.city.name,).add_to(map)
    folium.PolyLine(locations=[[start.city.latitude, start.city.longitude], [end.city.latitude, end.city.longitude]], color='blue', dash_array=[5, 5]).add_to(map)
    # Return the HTML as a HttpResponse
    return HttpResponse(map._repr_html_())

def get_route_map(request):
    # Get route from GET request
    route = request.GET.get('route')
    # Convert route to an array using ast (get params are always string, even though formatted [a,b,c])
    route_array = ast.literal_eval(route)
    # Get city objects for each city in string array
    cities = []
    for city in route_array:
        city_object = start_city = get_object_or_404(City, name = city)
        cities.append(city_object)
    # Use custom formula and distance to calculate a custom zoom level
    zoom = 6 - (lat_long_distance(cities[0].latitude, cities[0].longitude, cities[len(cities)-1].latitude, cities[len(cities)-1].longitude) / 500)
    # Create a map, with latitude and longitude centered around the start and end locations
    map = folium.Map(location=[(cities[0].latitude + cities[0].latitude) / 2, (cities[len(cities)-1].longitude + cities[len(cities)-1].longitude) / 2], zoom_start=zoom)
    # Loop through the city objects plotting each point
    for i, city in enumerate(cities):
        # Change icon based on type of travel and whether it is the start or the end of the journey
        if i == 0:
            folium.Marker(location=[city.latitude, city.longitude], popup=city.name, icon=folium.Icon(color='orange', icon='location-pin', prefix='fa'), tooltip=city.name,).add_to(map)
        elif i == len(cities)-1:
            folium.Marker(location=[city.latitude, city.longitude], popup=city.name, icon=folium.Icon(color='orange', icon='flag-checkered', prefix='fa'), tooltip=city.name,).add_to(map)
        else:
            route = get_object_or_404(TravelRoute, start_city = city, end_city = cities[i + 1])
            if route.type == "train":
                folium.Marker(location=[city.latitude, city.longitude], popup=city.name, icon=folium.Icon(color='orange', icon='train', prefix='fa'), tooltip=city.name,).add_to(map)
            else:
                folium.Marker(location=[city.latitude, city.longitude], popup=city.name, icon=folium.Icon(color='orange', icon='ship', prefix='fa'), tooltip=city.name,).add_to(map)
    # Loop through the city objects plotting routes between each
    for i in range (len(cities) - 1):
        folium.PolyLine(locations=[[cities[i].latitude, cities[i].longitude], [cities[i+1].latitude, cities[i+1].longitude]], color='blue', dash_array=[5, 5]).add_to(map)
    # Return the HTML as a HttpResponse
    return HttpResponse(map._repr_html_())

def full_map(request):
    # Create a map, with latitude and longitude centered on Europe
    map = folium.Map(location=[51,10], zoom_start=3)
    # Loop all cities
    for city in City.objects.all():
        folium.Marker(location=[city.latitude, city.longitude], popup=city.name, icon=folium.Icon(color='orange', icon='location-pin', prefix='fa'), tooltip=city.name,).add_to(map)
    for route in TravelRoute.objects.all():
        folium.PolyLine(locations=[[route.start_city.latitude, route.start_city.longitude], [route.end_city.latitude, route.end_city.longitude]], color='blue', dash_array=[5, 5]).add_to(map)
    # Return the HTML as a HttpResponse
    return HttpResponse(map._repr_html_())