from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def home(request):
    variable = "hello world"
    return render(request, 'index.html', {'variable':variable, 'title': 'Home'})
