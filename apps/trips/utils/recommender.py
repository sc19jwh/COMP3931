from sklearn.metrics.pairwise import cosine_similarity
from apps.trips.utils.geofuncs import dijkstra

# INPUT: trip object, queryset of cities, queryset of routes, sourc_city object, existing route as array of city objects
# OUTPUT: list of similarity scores between trip and cities
# e.g. recommend_next_destination(trip, cities, routes, source_city, existing_route)
def recommend_next_destination(trip, cities, routes, source_city, existing_route):
    # Remove the cities already in the trip from all cities
    other_cities = set(cities) - set(existing_route)
    # Find the shortest/longest journey possible by finding the duration from the source city to all other cities
    shortest_journey = float('inf')
    longest_journey = 0
    for city in other_cities:
        if city.name != source_city:
            route, duration = dijkstra(cities, routes, source_city.name, city.name)
            if duration > longest_journey:
                longest_journey = duration
            if duration < shortest_journey:
                shortest_journey = duration
    # Create the trip profile
    trip_profile = [trip.journey_times, trip.climate, trip.food_budget, trip.accom_budget]
    # Create empty array to store the similarities in
    similarities = []
    # Loop through all the
    for city in other_cities:
        route, duration = dijkstra(cities, routes, source_city.name, city.name)
        # Scale journey time against longest and shortest possible journey to get value between 0-100
        scaled_journey = ((duration - shortest_journey) / (longest_journey - shortest_journey)) * 100
        # Create city profile for the city (include journey time)
        city_profile = [scaled_journey, city.climate, city.food_budget, city.accom_budget]
        # Use cosine similarity to work out best cities
        cosine = cosine_similarity([trip_profile], [city_profile])[0][0]
        # Append the city and the final similarity value 
        similarities.append((cosine, city))
    # Sort by most similar first
    return sorted(similarities, key=lambda x: x[0], reverse=True)

# INPUT: trip object, queryset of cities
# OUTPUT: list of similarity scores between trip and cities
# e.g. recommend_first_destination(trip, cities)
def recommend_first_destination(trip, cities):
    # Create the trip profile
    trip_profile = [trip.climate, trip.food_budget, trip.accom_budget]
    # Create empty array to store the similarities in
    similarities = []
    # Loop through all the
    for city in cities:
        # Create city profile for the city
        city_profile = [city.climate, city.food_budget, city.accom_budget]
        # Use cosine similarity to work out best cities (regardless of journey time)
        cosine = cosine_similarity([trip_profile], [city_profile])[0][0]
        similarities.append((cosine, city))
    # Sort by most similar first
    return sorted(similarities, key=lambda x: x[0], reverse=True)