from django.shortcuts import render
from apps.authentication.models import Profile

def main(request):
    context = {'title': 'Home', 'profile': Profile.objects.get(user=request.user)}
    return render(request, 'main.html', context)

def features(request):
    context = {'title': 'Home', 'profile': Profile.objects.get(user=request.user)}
    return render(request, 'features.html', context)

def showcase1(request):
    context = {'title': 'Home', 'profile': Profile.objects.get(user=request.user)}
    return render(request, 'showcase1.html', context)

def faqs(request):
    context = {'title': 'Home', 'profile': Profile.objects.get(user=request.user)}
    return render(request, 'faqs.html', context)

def join(request):
    context = {'title': 'Home', 'profile': Profile.objects.get(user=request.user)}
    return render(request, 'join.html', context)