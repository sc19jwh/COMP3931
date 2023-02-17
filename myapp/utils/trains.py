import requests
from bs4 import BeautifulSoup

url = "https://www.interrail.eu/en/plan-your-trip/interrail-timetable?ol=LONDON+KINGS+CROSS+%28UNITED+KINGDOM%29&ov=007061210&dl=NEWCASTLE+%28UNITED+KINGDOM%29&dv=007084870&vl=&vv=&t=1676116800000&ar=false&rt=&tt=&mc=&mct=0#/"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

journey_cards = soup.find("div", class_="journey__cards")
print(journey_cards)

