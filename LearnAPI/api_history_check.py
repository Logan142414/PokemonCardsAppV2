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
    "setId": 1409,
    "fetchAllInSet": "true"
}
response = requests.get(f"{PokemonK_URL}/sealed-products", headers=headers, params=params)
data = response.json()
products = data.get("data", [])

############

# for p in products:
#     if p.get("tcgPlayerId") == "649295":
#         print(f"Product: {p.get('name')}")
#         print(f"Price History: {p.get('priceHistory')}")
#         break

# for p in products:
#     if p.get("tcgPlayerId") == "693146":
#         print(f"Product: {p.get('name')}")
#         print(f"Price History entries: {len(p.get('priceHistory', []))}")
#         print(f"Price History: {p.get('priceHistory')}")
#         break

# for p in products:
#     if p.get("tcgPlayerId") == "693146":
#         print(json.dumps(p, indent=2))
#         break

for p in products:
    if p.get("tcgPlayerId") == "98580":
        print(json.dumps(p, indent=2))
        break
    
# print(f"Total products returned: {len(products)}")
# for p in products:
#     print(p.get("tcgPlayerId"), p.get("name"))