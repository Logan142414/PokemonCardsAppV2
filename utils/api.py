import os
from dotenv import load_dotenv
import requests
import time


load_dotenv()
PokemonK = os.getenv("Pokemon_K")
PokemonK_URL = os.getenv("Pokemon_K_URL")


# get the card data for each of the sets
def get_card_data(set_num):
    
    headers = {"Authorization": f"Bearer {PokemonK}"}
    url = f"{PokemonK_URL}/api/v2/cards"

    for i in set_num:
        params = {"language": "english",
                "fetchAllInSet": "true",
                "sortBy": "price",
                "sortOrder": "desc",
                "setId": i,
                "minPrice": 0.99}

        response = requests.get(url, headers = headers, params = params)
        data = response.json()

        if response.status_code == 429:
            retry_after = data.get("retryAfter", 60)
            print(f"  Rate limited — waiting {retry_after}s")
            time.sleep(retry_after)
            response = requests.get(url, headers=headers, params=params)
            data = response.json()

        if response.status_code == 403:
            print(f"  BLOCKED: {data.get('message')} — stopping")
            return

        if response.status_code != 200:
            print(f"  API ERROR {response.status_code}: {data}")
            yield i, []
            time.sleep(2)
            continue

        cards = data.get("data", [])
        credits_used = response.headers.get("X-API-Calls-Consumed", "?")
        credits_remaining = response.headers.get("X-RateLimit-Daily-Remaining", "?")
        set_name = cards[0].get("setName") if cards else str(i)
        print(f"  Set {set_name}: {len(cards)} cards fetched | Credits used: {credits_used} | Remaining: {credits_remaining}")
        yield i, cards
        time.sleep(2)



def fetch_sets():
            
    headers = {"Authorization": f"Bearer {PokemonK}"}
    url = f'{PokemonK_URL}/api/v2/sets'

    params = {
                "language": "english",
                "sortBy": "releaseDate",
                "sortOrder": "desc",
                "limit": 500
            }
    
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"API ERROR {response.status_code}: {response.json()}")
        return []

    data = response.json()
    return data["data"]



# def get_sealed_data():

#     headers = {"Authorization": f"Bearer {PokemonK}"}
#     url = f"{PokemonK_URL}/api/v2/cards"


