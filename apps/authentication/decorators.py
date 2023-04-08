from django.shortcuts import redirect
from django.urls import reverse

def nationality_required(view):
    def wrap_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.nationality is not None:
            return view(request, *args, **kwargs)
        return redirect('setcountry')
    return wrap_view

def no_login_required(view):
    def wrap_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view(request, *args, **kwargs)
        return redirect('mytrips', request.user.username)
    return wrap_view