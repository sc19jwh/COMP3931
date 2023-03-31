import requests
import json
import datetime

# INPUT: session_token string derived from 'quick search' and True/False value for direct flights 
# OUTPUT: 2 dictionaries of flight information
# e.g. full_flight_search(session_token, True)
def full_flight_search(session_token, direct):
    # Create url by combining base url and session_token from previous step
    url = "https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/poll/" + session_token
    headers = {
        "x-api-key": "prtl6749387986743898559646983194"
    }
    # Load as JSON
    response = json.loads(requests.post(url, headers=headers).text)
    # Call process function
    session_token, direct_flights, connecting_flights = process_response(response, direct)
    # Return the values returned from process function apart from session_token as will no longer be needed
    return direct_flights, connecting_flights

# INPUT: strings for currency, IATA Codes for departure/destination, integers for year/month/day, boolean for direct flights
# OUTPUT: 2 dictionaries of flight information and a session_token of the search
# e.g. quick_flight_search("GBP", "MAN", "NAP", 2023, 6, 12, True)
def quick_flight_search(currency, departure_code, destination_code, year, month, day, direct):
    # URL 
    url = "https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create"
    # Using pulic API key
    headers = {
        "x-api-key": "prtl6749387986743898559646983194"
    }
    # Search data
    data = {
        "query": {
            "market": "UK",
            "locale": "en-GB",
            "currency": currency,
            "query_legs": [{
                "origin_place_id": {"iata": departure_code},
                "destination_place_id": {"iata": destination_code},
                "date": {"year": year, "month": month, "day": day}
            }],
            "adults": 1,
            "cabin_class": "CABIN_CLASS_ECONOMY"
        }
    }
    # response = requests.post(url, headers=headers, json=data)
    response = json.loads(requests.post(url, headers=headers, json=data).text)
    # Call process function
    session_token, direct_flights, connecting_flights = process_response(response, direct)
    # Return the values returned from process function
    return session_token, direct_flights, connecting_flights

# INPUT: response from API call and boolean value of whether returns should only include direct flights
# OUTPUT: 2 dictionaries of flight information and a session_token of the search
# e.g. session_token, direct_flights, connecting_flights = process_response(response, direct)
def process_response(response, direct):
    # Save itineraries (price), legs (total journey path), segment (flights within a leg), carriers (airlines)
    # and places (where flights are going to and from)
    try:
        session_token = response["sessionToken"]
        itineraries = response["content"]["results"]["itineraries"]
        legs = response["content"]["results"]["legs"]
        segments = response["content"]["results"]["segments"]
        carriers = response["content"]["results"]["carriers"]
        places = response["content"]["results"]["places"]
    except KeyError:
        session_token = ""
        direct_flights = []
        connecting_flights = []
        return session_token, direct_flights, connecting_flights
    # Create flights dict
    direct_flights = []
    connecting_flights = []
    # Loop itineraries
    for key, value in itineraries.items():
        # Save cheapest price from itinerary
        cheapest_price = float(itineraries[key]["pricingOptions"][0]["price"]["amount"]) / 1000
        link = itineraries[key]["pricingOptions"][0]["items"][0]["deepLink"]
        # Get leg id from itinerary
        leg_id = itineraries[key]["legIds"][0]
        # Check if direct flight
        if legs[leg_id]["stopCount"] == 0:
            # Find and format departure/arrival time from leg
            departure_time = datetime.datetime(**legs[leg_id]["departureDateTime"]).strftime('%Y-%m-%d %H:%M:%S')
            arrival_time = datetime.datetime(**legs[leg_id]["arrivalDateTime"]).strftime('%Y-%m-%d %H:%M:%S')
            duration = legs[leg_id]["durationInMinutes"]
            # Find carrier id from leg
            carrier_id = legs[leg_id]["operatingCarrierIds"][0]
            # Find name of carrier from carrier id
            carrier = carriers[carrier_id]["name"]
            # Find carrier logo
            carrier_logo = carriers[carrier_id]["imageUrl"]
            # Create flight object and append to flights dict
            flight = {"link": link,
                    "price": cheapest_price, 
                    "departure_time": departure_time, 
                    "arrival_time": arrival_time,
                    "duration": duration, 
                    "airline": carrier,
                    "airline_logo": carrier_logo}
            direct_flights.append(flight)
        # Find connecting flights if direct only filter is not on
        elif legs[leg_id]["stopCount"] > 0 and direct == False:
            # Get primary information such as total duration and start/end times
            departure_time = datetime.datetime(**legs[leg_id]["departureDateTime"]).strftime('%Y-%m-%d %H:%M:%S')
            arrival_time = datetime.datetime(**legs[leg_id]["arrivalDateTime"]).strftime('%Y-%m-%d %H:%M:%S')
            duration = legs[leg_id]["durationInMinutes"]
            # Get all flights in the trip
            segment_ids = legs[leg_id]["segmentIds"]
            # Initialise dict to store sub_flights
            sub_flights = []
            for segment_id in segment_ids:
                # Find the place IDs
                segment_departure_airport_id = segments[segment_id]["originPlaceId"]
                segment_arrival_airport_id = segments[segment_id]["destinationPlaceId"]
                # Find the place names
                segment_departure_airport = places[segment_departure_airport_id]["name"]
                segment_arrival_airport = places[segment_arrival_airport_id]["name"]
                # Find the departure and arrival times of the individual flights
                segment_departure_time = datetime.datetime(**segments[segment_id]["departureDateTime"]).strftime('%Y-%m-%d %H:%M:%S')
                segment_arrival_time = datetime.datetime(**segments[segment_id]["arrivalDateTime"]).strftime('%Y-%m-%d %H:%M:%S')
                # Find the airline ID and airline name
                carrier_id = segments[segment_id]["operatingCarrierId"]
                carrier = carriers[carrier_id]["name"]
                # Add sub_flight dictionary
                sub_flight = {"departure_airport": segment_departure_airport,
                    "arrival_airport": segment_arrival_airport,
                    "departure_time": segment_departure_time, 
                    "arrival_time": segment_arrival_time, 
                    "airline": carrier}
                sub_flights.append(sub_flight)
            # Append to overal flights dict with all information including sub_flights dict
            flight = {"link": link,
                    "price": cheapest_price, 
                    "departure_time": departure_time, 
                    "arrival_time": arrival_time,
                    "duration": duration, 
                    "stop_count": legs[leg_id]["stopCount"],
                    "sub_flights": sub_flights}
            connecting_flights.append(flight)
    # Return session_token and resulting dicts
    return session_token, direct_flights, connecting_flights