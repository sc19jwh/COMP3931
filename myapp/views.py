# Django imports
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
# Other imports
import base64
import time
# Folder imports
from .utils.currency import *
from .utils.cities import *
from .models import *
from .forms import CreateUserForm, AuthenticationForm

def home(request):
    print(getExchangeRates("EUR")["USD"])
    countries = Country.objects.filter()
    context = {'title': 'Home', 'countries': countries}
    return render(request, 'index.html', context)

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
    return render(request, 'user_auth/signin.html', context)

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
                return redirect('home')
    context = {'title': 'Register', 'form': form}
    return render(request, 'user_auth/register.html', context)

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
    return render(request, 'user_auth/profile.html', context)