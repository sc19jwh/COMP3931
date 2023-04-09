from sklearn.metrics.pairwise import cosine_similarity
from apps.trips.utils.geofuncs import dijkstra

# INPUT: trip object, queryset of cities, queryset of routes, sourc_city object, existing route as array of city objects
# OUTPUT: list of similarity scores between trip and cities
# e.g. recommend_next_destination(trip, cities, routes, source_city, existing_route)
def recommend_next_destination(trip, cities, routes, source_city, existing_route):
    # Remove the cities already in the trip from all cities
    other_cities = set(cities) - set(existing_route)
    # Find the longest journey possible by finding the duration from the source city to all other cities
    longest_journey = 0
    for city in other_cities:
        if city.name != source_city:
            route, duration = dijkstra(cities, routes, source_city.name, city.name)
            if duration > longest_journey:
                longest_journey = duration
    # Create the trip profile
    trip_profile = [trip.budget, trip.climate, trip.food_culture, trip.tourist_attractions, trip.nightlife_level]
    # Create empty array to store the similarities in
    similarities = []
    # Loop through all the
    for city in other_cities:
        # Create city profile for the city
        city_profile = [city.budget, city.climate, city.food_culture, city.tourist_attractions, city.nightlife_level]
        # Use cosine similarity to work out best cities (regardless of journey time)
        cosine = cosine_similarity([trip_profile], [city_profile])[0][0]
        # Use dijkstra to find the shortest duration between the source city and city
        route, duration = dijkstra(cities, routes, source_city.name, city.name)
        # Combine the cosine similarity, duration and wilingness to travel long journeys to get final result
        combined = ((cosine * (100 - float(trip.journey_times))/100) + ((1 - (duration / longest_journey)) * float(trip.journey_times))/100)
        # Append the city and the final similarity value 
        similarities.append((combined, city))
    # Sort by most similar first
    similarities.sort(reverse=True)
    return similarities

# INPUT: trip object, queryset of cities
# OUTPUT: list of similarity scores between trip and cities
# e.g. recommend_first_destination(trip, cities)
def recommend_first_destination(trip, cities):
    # Create the trip profile
    trip_profile = [trip.budget, trip.climate, trip.food_culture, trip.tourist_attractions, trip.nightlife_level]
    # Create empty array to store the similarities in
    similarities = []
    # Loop through all the
    for city in cities:
        # Create city profile for the city
        city_profile = [city.budget, city.climate, city.food_culture, city.tourist_attractions, city.nightlife_level]
        # Use cosine similarity to work out best cities (regardless of journey time)
        cosine = cosine_similarity([trip_profile], [city_profile])[0][0]
        similarities.append((cosine, city))
    # Sort by most similar first
    similarities.sort(reverse=True)
    return similarities