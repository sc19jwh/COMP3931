from geopy.geocoders import Nominatim

# INPUT: city as string
# OUTPUT: two variables for latitude and longitude
# e.g. long, lat = get_long_lat("Budapest")
def get_long_lat(city):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude