from django.shortcuts import render, redirect
from apps.authentication.models import Profile
from apps.authentication.decorators import no_login_required

@no_login_required
def main(request):
    context = {'title': 'Home'}
    return render(request, 'main.html', context)

def features(request):
    context = {'title': 'Home'}
    return render(request, 'features.html', context)

def showcase1(request):
    context = {'title': 'Home'}
    return render(request, 'showcase1.html', context)

def faqs(request):
    context = {'title': 'Home'}
    return render(request, 'faqs.html', context)