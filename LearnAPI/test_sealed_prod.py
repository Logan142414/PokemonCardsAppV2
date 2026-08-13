import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()
PokemonK = os.getenv("Pokemon_K")
PokemonK_URL = os.getenv("Pokemon_K_URL")

# Test with 3 set numeric IDs from your sets table
test_sets = [23651]  # sv08-surging-sparks, sv08.5-prismatic-evolutions, sv07-stellar-crown

headers = {"Authorization": f"Bearer {PokemonK}"}
url = f"{PokemonK_URL}/sealed-products"

for set_id in test_sets:
    params = {
        "language": "english",
        "setId": set_id,
        "sortBy": "price",
        "sortOrder": "desc", 
        "limit" : 1
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if response.status_code != 200:
        print(f"ERROR {response.status_code}: {data}")
        continue

    products = data.get("data", [])
    credits_used = response.headers.get("X-API-Calls-Consumed", "?")
    credits_remaining = response.headers.get("X-RateLimit-Daily-Remaining", "?")
    print(f"\nSet {set_id}: {len(products)} products | Credits used: {credits_used} | Remaining: {credits_remaining}")
    
    print(products)

    time.sleep(2)