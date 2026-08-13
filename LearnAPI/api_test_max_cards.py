import requests
from dotenv import load_dotenv
import os

load_dotenv()

Pokemon_K = os.getenv("Pokemon_K")
Pokemon_K_URL = os.getenv("Pokemon_K_URL")

params = {
    "language": "english",
    "fetchAllInSet": "true",
    "setId": 22880,
    "minPrice": 0.99
}

headers = {"Authorization": f"Bearer {Pokemon_K}"}
url = f"{Pokemon_K_URL}/cards"

response = requests.get(url, headers=headers, params=params)
data = response.json()
print(len(data.get("data", [])))
print(data["metadata"]["total"])  # total matching cards in the set
print(data["metadata"]["hasMore"])