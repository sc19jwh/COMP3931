from geopy.geocoders import Nominatim
import gmplot

# INPUT: city as string
# OUTPUT: two variables for latitude and longitude
# e.g. long, lat = get_long_lat("Budapest")
def get_long_lat(city):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude

# INPUT:
# OUTPUT: 
# e.g. 
def plotmap():
    gmap = gmplot.GoogleMapPlotter(48.2082, 16.3738, 4.5)

    budapest_lat, budapest_lon = get_long_lat("Budapest")
    madrid_lat, madrid_lon = get_long_lat("Madrid")
    london_lat, london_lon = get_long_lat("London")
    kenilworth_lat, kenilworth_lon = get_long_lat("Kenilworth, UK")

    gmap.marker(budapest_lat, budapest_lon, 'red')
    gmap.marker(madrid_lat, madrid_lon, 'red')
    gmap.marker(london_lat, london_lon, 'red')
    gmap.marker(kenilworth_lat, kenilworth_lon, 'red')

    gmap.plot([budapest_lat, madrid_lat], [budapest_lon, madrid_lon], edge_color='blue')
    gmap.plot([budapest_lat, london_lat], [budapest_lon, london_lon], edge_color='blue')
    gmap.plot([madrid_lat, kenilworth_lat], [madrid_lon, kenilworth_lon], edge_color='blue')

    gmap.draw("europe_map.html")
