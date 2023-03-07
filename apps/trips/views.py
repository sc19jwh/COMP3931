# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.db.models import Min, Max
from django.template.loader import render_to_string
# Other imports
import base64
# Folder imports
from .models import *
from apps.authentication.models import Profile

def home(request):
    countries = Country.objects.filter(is_interrail=True)
    context = {'title': 'Home', 'countries': countries}
    return render(request, 'index.html', context)

def mytrips(request, username):
    if not request.user.is_authenticated:
        return redirect('signin')
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

def configtrip(request, trip_id, username):
    start_city = City.objects.get(name="Oslo")
    end_city = City.objects.get(name="Hamburg")
    direct_route = TravelRoute.objects.filter(start_city=start_city, end_city=end_city).first()
    if direct_route:
        print(direct_route.start_city.name + " - " + direct_route.end_city.name)
    else:
        for route in TravelRoute.objects.filter(start_city=start_city):
            connection = TravelRoute.objects.filter(start_city=route.end_city, end_city=end_city).first()
            if connection:
                duration = route.duration + connection.duration
                print(route.start_city.name + " - " + route.end_city.name + " ({} mins)".format(route.duration))
                print(connection.start_city.name + " - " + connection.end_city.name + " ({} mins)".format(connection.duration))

    if not request.user.is_authenticated:
        return redirect('signin')
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
    # destination_photos = []
    # for destination in trip.destination_set.all():
    #     destination_photos.append(search_unsplash(destination.city.name))
    # Check if the trip belongs to the current user
    context = {'title': 'My Trips', 'trip': trip,'countries': countries, 'profile': Profile.objects.get(user=request.user)}
    return render(request, 'configtrip.html', context)

def cities(request):
    country = request.GET.get('country')
    cities = City.objects.filter(country=country)
    context = {'cities': cities}
    return render(request, 'partials/cities.html', context)