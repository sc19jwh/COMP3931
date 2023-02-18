import requests
from bs4 import BeautifulSoup

url = "https://www.rome2rio.com/map/Split/Ancona"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
deeplink_meta = soup.find("meta", attrs={"id": "deeplinkTrip"})

with open("output.txt", "w") as file:
    file.write(str(soup))
