import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
PokemonK = os.getenv("Pokemon_K")
PokemonK_URL = os.getenv("Pokemon_K_URL")

headers = {"Authorization": f"Bearer {PokemonK}"}

# params = {
#     "language": "english",
#     "includeHistory": "true",
#     "days": 180,
#     "setId": 2374,
#     "fetchAllInSet": "true"
# }

#############
# params = {
#     "language": "english",
#     "includeHistory": "true",
#     "days": 180,
#     "setId": 1815,
#     "fetchAllInSet": "true"
# }

params = {
    "language": "english",
    "includeHistory": "true",
    "days": 180,
    "setId": 2282,
    "fetchAllInSet": "true",
}
response = requests.get(f"{PokemonK_URL}/cards", headers=headers, params=params)
data = response.json()
cards = data.get("data", [])

print(f"Total cards returned: {len(cards)}")
# for c in cards:
#     print(c.get("tcgPlayerId"), c.get("name"))