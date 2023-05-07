# Django imports
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
# Other imports
import folium
import ast
# Folder imports
from apps.trips.models import *
from apps.trips.utils.geofuncs import lat_long_distance

# URL: maps/partials/get_travel_map
# HTTP Method: GET
# Description: Generate map for start and end destination
def get_travel_map(request):
    # Get the start and end point destination IDs
    start_id = request.GET.get('start')
    end_id = request.GET.get('end')
    if start_id is None or end_id is None:
        return HttpResponseBadRequest("Missing start and/or end parameters.")
    # Get the destination objects
    start = get_object_or_404(Destination, id=start_id)
    end = get_object_or_404(Destination, id=end_id)
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

# URL: partials/features
# HTTP Method: GET
# Description: Generate map for route between two destinations including transfer stations
def get_route_map(request):
    # Get route from GET request
    route = request.GET.get('route')
    if route is None:
        return HttpResponseBadRequest("Missing route.")
    # Convert route to an array using ast (get params are always string, even though formatted [a,b,c])
    route_array = ast.literal_eval(route)
    # Get city objects for each city in string array
    cities = []
    for city in route_array:
        city_object = get_object_or_404(City, name = city)
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

# URL: partials/features
# HTTP Method: GET
# Description: Generate map for all interrail cities and travel routes
def full_map(request):
    # Create a map, with latitude and longitude centered on Europe
    map = folium.Map(location=[51,10], zoom_start=4)
    # Loop all cities
    for city in City.objects.all():
        folium.Marker(location=[city.latitude, city.longitude], popup=city.name, icon=folium.Icon(color='orange', icon='location-pin', prefix='fa'), tooltip=city.name,).add_to(map)
    for route in TravelRoute.objects.all():
        folium.PolyLine(locations=[[route.start_city.latitude, route.start_city.longitude], [route.end_city.latitude, route.end_city.longitude]], color='blue', dash_array=[5, 5]).add_to(map)
    # Return the HTML as a HttpResponse
    return HttpResponse(map._repr_html_())

# URL: partials/features
# HTTP Method: GET
# Description: Generate summary map for all cities on trip
def get_trip_map(request):
    # Get TRIP from GET request
    trip_id = request.GET.get('trip_id')
    if trip_id is None:
        return HttpResponseBadRequest("Missing trip id.")
    trip = get_object_or_404(Trip, id = trip_id)
    cities = []
    for destination in Destination.objects.filter(trip=trip):
        city = destination.city
        cities.append(city)
    # Use custom formula and distance to calculate a custom zoom level
    zoom = 6 - (lat_long_distance(cities[0].latitude, cities[0].longitude, cities[len(cities)-1].latitude, cities[len(cities)-1].longitude) / 500)
    # Create a map, with latitude and longitude centered around the start and end locations
    map = folium.Map(location=[(cities[0].latitude + cities[0].latitude) / 2, (cities[len(cities)-1].longitude + cities[len(cities)-1].longitude) / 2], zoom_start=zoom)
    # Loop through the city objects plotting each point
    for i, city in enumerate(cities):
        folium.Marker(location=[city.latitude, city.longitude], popup=city.name, icon=folium.Icon(color='orange', icon=str(i+1), prefix='fa'), tooltip=city.name,).add_to(map)
    # Loop through the city objects plotting routes between each
    for i in range (len(cities) - 1):
        folium.PolyLine(locations=[[cities[i].latitude, cities[i].longitude], [cities[i+1].latitude, cities[i+1].longitude]], color='blue', dash_array=[5, 5]).add_to(map)
    # Return the HTML as a HttpResponse
    # return HttpResponse(200)
    return HttpResponse(map._repr_html_())