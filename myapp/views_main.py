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
from .utils.currency import *
from .models import *
from .forms import CreateUserForm, AuthenticationForm

def home(request):
    countries = Country.objects.filter(is_interrail=True)
    context = {'title': 'Home', 'countries': countries}
    return render(request, 'main/index.html', context)

def signin(request):
    warning = False
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = AuthenticationForm()
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    print("user")
                    login(request, user)
                    return redirect('home')
            else:
                warning = True
    context = {'title': 'Login', 'form': form, 'warning': warning}
    return render(request, 'main/user_auth/signin.html', context)

def signout(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    # Get user creation form from forms.py
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        # If valid account made
        if form.is_valid():
            # Save account
            form.save()
            # Then login user
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            # Create Profile for user
            Profile.objects.create(user=user)
            if user is not None:
                login(request, user)
                return redirect('setcountry')
    context = {'title': 'Register', 'form': form}
    return render(request, 'main/user_auth/register.html', context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        image_data = request.FILES['photo'].read()
        base64_data = base64.b64encode(image_data).decode()
        user_profile = request.user.profile
        user_profile.image = base64_data
        user_profile.save()
    context = {'title': 'User Profile', 'profile': Profile.objects.get(user=request.user)}
    return render(request, 'main/user_auth/profile.html', context)

def setcountry(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        selected_country_pk = request.POST.get('country')
        selected_country = Country.objects.get(pk=selected_country_pk)
        profile = request.user.profile
        profile.nationality = selected_country
        profile.save()
        return redirect('home')
    current_user_nationality = Profile.objects.get(user=request.user).nationality
    countries = Country.objects.filter()
    context = {'title': 'Set Country', 'countries': countries, 'current_user_nationality': current_user_nationality}
    return render(request, 'main/user_auth/setcountry.html', context)

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
    return render(request, 'main/trips/mytrips.html', context)

def currency(request):
    countries = Country.objects.all()
    context = {'title': 'Currency', 'countries': countries, 'profile': Profile.objects.get(user=request.user)}
    return render(request, 'main/currency/manual.html', context)

def configtrip(request, trip_id, username):
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
    # Check if the trip belongs to the current user
    context = {'title': 'My Trips', 'trip': trip,'countries': countries, 'profile': Profile.objects.get(user=request.user)}
    return render(request, 'main/trips/configtrip.html', context)