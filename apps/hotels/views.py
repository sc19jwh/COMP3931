# Django imports
from django.shortcuts import render, get_object_or_404
from .utils.hotels import quick_hotel_search, full_hotel_search
# Other imports
from datetime import date
# Folder imports
from apps.trips.models import Destination

def search_hotel(request):
    destination_id = request.GET.get('destination_id')
    destination = get_object_or_404(Destination, id = destination_id)
    if destination.start_date > date.today():
        session_token, hotels = quick_hotel_search("GBP", str(destination.city.skyscanner_id), destination.start_date.year, destination.start_date.month, destination.start_date.day, destination.end_date.year, destination.end_date.month, destination.end_date.day)
    context = {'hotels': hotels, 'destination': destination, 'city': destination.city}
    return render(request, 'partials/search_hotel.html', context)