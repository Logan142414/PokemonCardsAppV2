import os
import requests
from dotenv import load_dotenv

load_dotenv()

PokemonK = os.getenv("Pokemon_K")
PokemonK_URL = os.getenv("Pokemon_K_URL")
headers = {"Authorization": f"Bearer {PokemonK}"}

test_cards = [
    {"search": "Charizard VMAX", "set": "Prize Pack Series Cards"},
    {"search": "Latias Star", "set": "World Championship Decks"},
    {"search": "Dark Blastoise", "set": "Jumbo Cards"},
]

for card in test_cards:
    params = {"language": "english", "search": card["search"], "set": card["set"]}
    response = requests.get(f"{PokemonK_URL}/api/v2/cards", headers=headers, params=params)
    data = response.json()
    cards = data.get("data", [])
    if cards:
        print(f"\n=== {card['search']} ===")
        print(cards[0])
    else:
        print(f"\n=== {card['search']} === NO RESULTS")