from geopy.geocoders import Nominatim
import h3
import networkx as nx

# INPUT: city as string
# OUTPUT: two variables for latitude and longitude
# e.g. long, lat = get_long_lat("Budapest")
def get_lat_long(city):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude

# INPUT: lat and long of two places
# OUTPUT: distance between the two points in km
# e.g. distance - lat_long_distance(52.4796992, -1.9026911, 53.31067150, -4.6330966)
def lat_long_distance(lat1, long1, lat2, long2):
    distance = h3.point_dist((lat1, long1), (lat2, long2), unit='km')
    return distance

# INPUT: queryset of all saved cities and routes, string of start city and string of end city
# OUTPUT: shortest path between two cities represented as an array
# e.g. dijkstra(cities, routes, "Paris", "Madrid")
def dijkstra(cities, routes, city1, city2):
    # Initialize a graph
    G = nx.DiGraph()
    # Loop through each city and create a node
    for city in cities:
        G.add_node(city.name)
    # Add weighted edges for routes between cities
    for route in routes:
        G.add_edge(route.start_city.name, route.end_city.name, weight=route.duration)

    # Use Dijkstra's
    return nx.shortest_path(G, source=city1, target=city2, weight="weight")

# INPUT: queryset of all saved cities and routes, string of start city and string of end city
# OUTPUT: shortest path between two cities represented as an array
# e.g. dijkstra(cities, routes, "Paris", "Madrid")
def least_transfers(cities, routes, city1, city2):
    # Initialize a graph
    G = nx.DiGraph()
    # Loop through each city and create a node
    for city in cities:
        G.add_node(city.name)
    # Add edges all with a weight of 1
    for route in routes:
        G.add_edge(route.start_city.name, route.end_city.name, weight=1)

    # Loop through the shortest path and sum the weights
    # duration = 0
    # for i in range(len(path)-1):
    #     duration += G.get_edge_data(path[i], path[i+1])['weight']

    # Use Dijkstra's to find the minimum number of connections
    return nx.shortest_path(G, source=city1, target=city2, weight="weight")