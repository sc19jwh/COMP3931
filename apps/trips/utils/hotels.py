import requests
import json
import datetime

# -----------------------------------
# NOTES: 
# - Function using SkyScanner API via RapidAPI (https://rapidapi.com/blog/skyscanner-api-overview/)
# - quick_hotel_search CREATES a search finds top results and returns a session_token
# - full_hotel_search POLLs a search using the session_token to find all results
# - As processing is uniform, a seperate function is used to process the response of either function (process_response) 
# -----------------------------------

# INPUT:  
# OUTPUT: 
# e.g. 
def quick_hotel_search(currency, place_id, checkin_year, checkin_month, checkin_day, checkout_year, checkout_month, checkout_day):
    url = "https://skyscanner-api.p.rapidapi.com/v3e/hotels/live/search/create"
    payload = {"query": {
            "market": "UK",
            "locale": "en-GB",
            "currency": currency,
            "adults": 2,
            "placeId": {"entityId": place_id},
            "checkInDate": {
                "year": checkin_year,
                "month": checkin_month,
                "day": checkin_day
            },
            "checkOutDate": {
                "year": checkout_year,
                "month": checkout_month,
                "day": checkout_day
            },
            "rooms": 1,
            "sortBy": "RELEVANCE_DESC"
        }}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "85b4ea59f1msh4671a05e50478ffp155b8fjsne76f959df8ac",
        "X-RapidAPI-Host": "skyscanner-api.p.rapidapi.com"
    }

    response = json.loads(requests.request("POST", url, json=payload, headers=headers).text)

    session_token = response["sessionToken"]
    hotels = response["content"]["results"]["hotels"]
    return session_token, hotels

# INPUT:  
# OUTPUT: 
# e.g. 
def full_hotel_search(session_token, page_number):
    url = "https://skyscanner-api.p.rapidapi.com/v3e/hotels/live/search/poll/" + page_number + "/" + session_token
    headers = {
        "X-RapidAPI-Key": "85b4ea59f1msh4671a05e50478ffp155b8fjsne76f959df8ac",
        "X-RapidAPI-Host": "skyscanner-api.p.rapidapi.com"
    }

    response = json.loads(requests.request("GET", url, headers=headers).text)
    hotels = response["content"]["results"]["hotels"]
    return hotels

# INPUT: string of a city name
# OUTPUT: dict of places matching the city name, along with it's country and the id
# e.g. skyscanner_id_finder("Stockholm")
def skyscanner_id_finder(city_name):
    url = "https://skyscanner-api.p.rapidapi.com/v3/geo/hierarchy/flights/en-GB"
    headers = {
        "X-RapidAPI-Key": "85b4ea59f1msh4671a05e50478ffp155b8fjsne76f959df8ac",
        "X-RapidAPI-Host": "skyscanner-api.p.rapidapi.com"
    }
    response = json.loads(requests.request("GET", url, headers=headers).text)
    places = response["places"]
    found_places = []
    for key, value in places.items():
        city = places[key]["name"]
        entityId = places[key]["entityId"]
        parentId = places[key]["parentId"]
        try:
            country = places[parentId]["name"]
        except KeyError:
            pass
        if city == city_name:
            place = {"city": city,
                    "country": country, 
                    "entityId": entityId}
            found_places.append(place)
    return found_places

places = skyscanner_id_finder("Tartu")
for place in places:
    print(place["city"], place["country"], place["entityId"])