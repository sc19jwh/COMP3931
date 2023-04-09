from django.shortcuts import redirect
from django.urls import reverse

# Decorator to redirect any page back to set country if user has not set their nationaity yet
def nationality_required(view):
    def wrap_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.nationality is not None:
            return view(request, *args, **kwargs)
        return redirect('setcountry')
    return wrap_view

# Decorator to redirect any logged in user back to the main dashboard if they are trying to access signin/register etc.
def no_login_required(view):
    def wrap_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view(request, *args, **kwargs)
        return redirect('mytrips', request.user.username)
    return wrap_view