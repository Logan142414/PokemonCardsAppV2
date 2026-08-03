#test out the api to get daily card prices
import http.client
from dotenv import load_dotenv
import os
import urllib

load_dotenv()
PokemonK = os.getenv("Pokemon_K")

conn = http.client.HTTPSConnection("www.pokemonpricetracker.com")

headers = {"Authorization": f"Bearer {PokemonK}"}

params = urllib.parse.urlencode({
    "language": "english",
    "grader": "PSA",   
    "limit": 2
})

conn.request("GET", f"/api/v2/parse-title?{params}", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))