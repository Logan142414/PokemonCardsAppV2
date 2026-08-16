import requests 
from dotenv import load_dotenv
from utils.database import get_set_ids_to_search
import os

load_dotenv()

# set_nums =get_set_ids_to_search()
set_nums = [23821]

class PokemonTrackerAPI:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {os.getenv("Pokemon_K")}"}
        self.base_url = os.getenv("Pokemon_K_URL")

    def get_past_price_history_test_sealed(self, set_nums):
                
                for set_num in set_nums:
                    params = {
                    "language": "english",
                    "includeHistory": "true",
                    "days" : 3,
                    "limit" : set_num,
                    "setId": set_num}

                    response = requests.get(f"{self.base_url}/sealed-products", headers=self.headers, params = params)
                    data = response.json()


                    # if response.status_code == 429:
                    #     retry_after = data.get("retryAfter", 60)
                    #     print(f"  Rate limited — waiting {retry_after}s")
                    #     time.sleep(retry_after)
                    #     response = requests.get(f"{self.base_url}/sealed-products", headers=self.headers, params=params)
                    #     data = response.json()

                    # if response.status_code == 403:
                    #     print(f"  BLOCKED: {data.get('message')} — stopping")
                    #     return

                    # if response.status_code != 200:
                    #     print(f"  API ERROR {response.status_code}: {data}")
                    #     yield set_num, []
                    #     time.sleep(2)
                    #     continue

                    products = data.get("data", [])
                    return products 


# api = PokemonTrackerAPI()
# r = api.get_past_price_history_test_sealed(set_nums)
# print(r)


#[{'id': '696fa93a98d6a52492c89e5b', 'tcgPlayerId': '593450', 'tcgPlayerUrl': 'https://www.tcgplayer.com/product/593450', 'name': 'Prismatic Evolutions Tech Sticker Collection [Sylveon]', 'setId': '23821', 
# 'setName': 'SV: Prismatic Evolutions', 'unopenedPrice': 41.71, 'imageCdnUrl': 'https://tcgplayer-cdn.tcgplayer.com/product/593450_in_200x200.jpg', 
# 'imageCdnUrl200': 'https://tcgplayer-cdn.tcgplayer.com/product/593450_in_200x200.jpg', 'imageCdnUrl400': 'https://tcgplayer-cdn.tcgplayer.com/product/593450_in_400x400.jpg', 
# 'imageCdnUrl800': 'https://tcgplayer-cdn.tcgplayer.com/product/593450_in_800x800.jpg', 'imageUrl': 'https://tcgplayer-cdn.tcgplayer.com/product/593450_in_200x200.jpg', 
# 'lastScrapedAt': '2026-08-06T12:47:13.329Z', 'createdAt': '2026-01-20T16:11:38.028Z', 'updatedAt': '2026-08-06T12:53:22.663Z', 
# 'priceHistory': [{'date': '2026-08-06T00:00:00.000Z', 'unopenedPrice': 41.71}]}, 
# 
# {'id': '696fa93998d6a52492c89e5a', 'tcgPlayerId': '598490', 'tcgPlayerUrl': 'https://www.tcgplayer.com/product/598490', 'name': 'Prismatic Evolutions Tech Sticker Collection [Set of 3]', 
# 'setId': '23821', 'setName': 'SV: Prismatic Evolutions', 'unopenedPrice': 130.16, 
# 'imageCdnUrl': 'https://tcgplayer-cdn.tcgplayer.com/product/598490_in_200x200.jpg', 'imageCdnUrl200': 'https://tcgplayer-cdn.tcgplayer.com/product/598490_in_200x200.jpg', 
# 'imageCdnUrl400': 'https://tcgplayer-cdn.tcgplayer.com/product/598490_in_400x400.jpg', 'imageCdnUrl800': 'https://tcgplayer-cdn.tcgplayer.com/product/598490_in_800x800.jpg', 'imageUrl': 'https://tcgplayer-cdn.tcgplayer.com/product/598490_in_200x200.jpg', 
# 'lastScrapedAt': '2026-08-06T12:47:13.329Z', 'createdAt': '2026-01-20T16:11:37.990Z', 'updatedAt': '2026-08-06T12:50:52.156Z', 
# 'priceHistory': [{'date': '2026-08-06T00:00:00.000Z', 'unopenedPrice': 130.16}]}]