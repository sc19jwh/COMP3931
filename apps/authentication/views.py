# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.db.models import Min, Max
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
# Other imports
import base64
# Folder imports
from apps.trips.models import Country
from .models import Profile
from .forms import CreateUserForm, AuthenticationForm
from .decorators import nationality_required, no_login_required

# URL: user/signin
# HTTP Method: GET, POST
# Description: Authenticates a user based on Django authentication form
@no_login_required
def signin(request):
    warning = False
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('mytrips', username)
        else:
            warning = True
    context = {'title': 'Login', 'form': form, 'warning': warning}
    return render(request, 'signin.html', context)

# URL: user/signout
# HTTP Method: GET
# Description: Signs out the current user and redirects to landing page
@login_required
def signout(request):
    logout(request)
    return redirect('main')

# URL: user/register
# HTTP Method: GET, POST
# Description: Facilitates user registration using CreateUserForm
@no_login_required
def register(request):
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
        else:
            errors = form.errors.as_data()
            context = {'title': 'Register', 'form': form, 'errors': errors}
            return render(request, 'register.html', context)
    context = {'title': 'Register', 'form': form}
    return render(request, 'register.html', context)

# URL: user/profile
# HTTP Method: GET, POST
# Description: Shows user account details and allows configuration of a profile image
@nationality_required
@login_required
def profile(request):
    if request.method == 'POST':
        image_data = request.FILES['photo'].read()
        base64_data = base64.b64encode(image_data).decode()
        user_profile = request.user.profile
        user_profile.image = base64_data
        user_profile.save()
    context = {'title': 'User Profile', 'profile': Profile.objects.get(user=request.user)}
    return render(request, 'profile.html', context)

# URL: user/setcountry
# HTTP Method: GET, POST
# Description: Allows user to configure their nationality
@login_required
def setcountry(request):
    if request.method == 'POST':
        selected_country_pk = request.POST.get('country')
        selected_country = Country.objects.get(pk=selected_country_pk)
        profile = request.user.profile
        profile.nationality = selected_country
        profile.save()
        return redirect('mytrips', request.user.username)
    current_user_nationality = Profile.objects.get(user=request.user).nationality
    countries = Country.objects.filter()
    context = {'title': 'Set Country', 'countries': countries, 'current_user_nationality': current_user_nationality}
    return render(request, 'setcountry.html', context)

# URL: user/partials/set_country_flag
# HTTP Method: GET
# Description: Facilitates live updating of user nationality flag as they select
def set_country_flag(request):
    id = request.GET.get('country')
    if not id:
        id = request.GET.get('country2')
    country = Country.objects.get(id=id)
    context = {'countryid': country.alpha2code}
    return render(request, 'partials/set_country_flag.html', context)