import requests
import http.client
import json
import urllib.parse
from dotenv import load_dotenv
import os
from utils.database import get_connection

load_dotenv()
PokemonK = os.getenv("Pokemon_K")

#headers is almost always = "Authorization: Bearer <the token>"
#params are what is added to the end of url after "?". Example is .../sets?language=english&minPrice=1
#body (never used for get requests). only when sending data. normally gets sent as json=...
#body parameters

#building connection with http.client
def test_with_httpclient():
    conn = http.client.HTTPSConnection("www.pokemonpricetracker.com")
    headers = {"Authorization": f"Bearer {PokemonK}"}
    params = urllib.parse.urlencode({"language":"english","limit":1})
    conn.request("GET", f"/api/v2/sets?{params}", headers=headers)
    res = conn.getresponse() #This waits for and receives the server's response
    data = json.loads(res.read().decode("utf-8")) #res.read() → reads the raw bytes from the response body, decode("utf-8") → converts those bytes into a readable string, json.loads(...) → converts that string into a Python dictionary
        

#building connection with requests
def test_with_requests():
    headers = {"Authorization": f"Bearer {PokemonK}"}
    params = {"language":"english", "limit": 1}
    response= requests.get("https://www.pokemonpricetracker.com/api/v2/sets", headers=headers, params=params)
    data = response.json()