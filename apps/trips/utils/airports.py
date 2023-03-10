import requests
from cities import get_lat_long

# INPUT: city as string
# OUTPUT: list of airports
# e.g.
# airports = get_nearby_airports("New York", 50)
# for airport in airports:
#         if 'iata_code' in airport:
#             print(airport['name'], airport['iata_code'], airport['distance'])
def get_nearby_airports(city, distance):
    # Get lat and long of a city using external function
    lat,lng = get_lat_long(city)
    # Pass parameters and api key to API
    api_key = 'd8fe8a72-7519-4391-a890-6e57ffaf8791'
    url = f'https://airlabs.co/api/v9/nearby?lat={lat}&lng={lng}&distance={distance}&api_key={api_key}'
    # Get and return airports
    airports = requests.get(url).json()['response']['airports']
    return airports