import os
import requests
from dotenv import load_dotenv

load_dotenv()

PokemonK = os.getenv("Pokemon_K")
PokemonK_URL = os.getenv("Pokemon_K_URL")
headers = {"Authorization": f"Bearer {PokemonK}"}

test_sets = [
    {"name": "ME: 30th Celebration", "numeric_id": 24722},
    {"name": "First Partner Collection 2026", "numeric_id": 24584},
    {"name": "MEE: Mega Evolution Energies", "numeric_id": 24461},
    {"name": "Trick or Trade BOOster Bundle 2023", "numeric_id": 23266},
    {"name": "e-Reader Sample Cards", "numeric_id": 24493},
]

for s in test_sets:
    params = {
        "language": "english",
        "setId": s["numeric_id"],
        "fetchAllInSet": "true",
        "sortBy": "price",
        "sortOrder": "desc",
    }
    response = requests.get(f"{PokemonK_URL}/cards", headers=headers, params=params)
    data = response.json()
    cards = data.get("data", [])
    print(f"\n=== {s['name']} ===")
    for card in cards[:3]:
        print(card)