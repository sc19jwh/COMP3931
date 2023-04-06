from geopy.geocoders import Nominatim
import h3
import networkx as nx

# INPUT: lat and long of two places
# OUTPUT: distance between the two points in km
# e.g. distance - lat_long_distance(52.4796992, -1.9026911, 53.31067150, -4.6330966)
def lat_long_distance(lat1, long1, lat2, long2):
    distance = h3.point_dist((lat1, long1), (lat2, long2), unit='km')
    return distance

# INPUT: queryset of all saved cities and routes, string of start city and string of end city
# OUTPUT: shortest path between two cities represented as an array and integer represnting journey duration (mins)
# e.g. dijkstra(cities, routes, "Paris", "Madrid")
def dijkstra(cities, routes, city1, city2):
    # Initialize a graph
    city_network = nx.DiGraph()
    # Loop through each city and create a node
    for city in cities:
        city_network.add_node(city.name)
    # Add weighted edges for routes between cities
    for route in routes:
        city_network.add_edge(route.start_city.name, route.end_city.name, weight=route.duration)
    # Use Dijkstra's to return shortest path and duration
    return nx.shortest_path(city_network, source=city1, target=city2, weight="weight"), nx.shortest_path_length(city_network, source=city1, target=city2, weight="weight")

# INPUT: queryset of all saved cities and routes, string of start city and string of end city
# OUTPUT: shortest path between two cities represented as an array and integer represnting journey duration (mins)
# e.g. dijkstra(cities, routes, "Paris", "Madrid")
def least_transfers(cities, routes, city1, city2):
    # Initialize a graph
    city_network = nx.DiGraph()
    # Loop through each city and create a node
    for city in cities:
        city_network.add_node(city.name)
    # Add edges all with a weight of 1
    for route in routes:
        city_network.add_edge(route.start_city.name, route.end_city.name)
    # Use Dijkstra's to find the minimum number of connections
    # Store the path instead of returning it straight away
    path = nx.shortest_path(city_network, source=city1, target=city2)
    duration = 0
    # Loop through cities in the path
    for i, city in enumerate(path):
        # Don't check final element as path[i+1] would go out of range
        if i < len(path) - 1:
            # Check routes to find route with start city and end city 
            for route in routes:
                if route.start_city.name == city and route.end_city.name == path[i + 1]:
                    # Once found add to duration
                    duration = duration + route.duration
    return path, duration