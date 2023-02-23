import requests

url = "https://flight-radar1.p.rapidapi.com/flights/search"

querystring = {"query":"FD3210","limit":"25"}

headers = {
	"X-RapidAPI-Key": "c3557821c7msh7f56c57b74e8a14p1a4334jsn88f0dafefb74",
	"X-RapidAPI-Host": "flight-radar1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)