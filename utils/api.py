import os
from dotenv import load_dotenv
import requests
import time


load_dotenv()

class PokemonTrackerAPI:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {os.getenv("Pokemon_K")}"}
        self.base_url = os.getenv("Pokemon_K_URL")

            
    # get the card data for each of the sets
    def api_get_card_data(self, set_num):
        
        for i in set_num:
            params = {"language": "english",
                    "fetchAllInSet": "true",
                    "sortBy": "price",
                    "sortOrder": "desc",
                    "setId": i,
                    "minPrice": 0.99}

            response = requests.get(f"{self.base_url}/cards", headers=self.headers, params = params)
            data = response.json()

            if response.status_code == 429:
                retry_after = data.get("retryAfter", 60)
                print(f"  Rate limited — waiting {retry_after}s")
                time.sleep(retry_after)
                response = requests.get(f"{self.base_url}/cards", headers=self.headers, params=params)
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



    def api_get_sets_data(self):
                

        params = {
                    "language": "english",
                    "sortBy": "releaseDate",
                    "sortOrder": "desc",
                    "limit": 500
                }
        
        response = requests.get(f"{self.base_url}/sets", headers=self.headers, params=params)

        if response.status_code != 200:
            print(f"API ERROR {response.status_code}: {response.json()}")
            return []

        data = response.json()
        return data["data"]



    def api_get_sealed_data(self, set_num):

        for i in set_num:
            params = {
            "language": "english",
            "setId": i,
            "fetchAllInSet": "true",
            "sortBy": "price",
            "sortOrder": "desc"
        }
            response = requests.get(f"{self.base_url}/sealed-products", headers=self.headers, params = params)
            data = response.json()

            if response.status_code == 429:
                retry_after = data.get("retryAfter", 60)
                print(f"  Rate limited — waiting {retry_after}s")
                time.sleep(retry_after)
                response = requests.get(f"{self.base_url}/sealed-products", headers=self.headers, params=params)
                data = response.json()

            if response.status_code == 403:
                print(f"  BLOCKED: {data.get('message')} — stopping")
                return

            if response.status_code != 200:
                print(f"  API ERROR {response.status_code}: {data}")
                yield i, []
                time.sleep(2)
                continue

            products = data.get("data", [])
            credits_used = response.headers.get("X-API-Calls-Consumed", "?")
            credits_remaining = response.headers.get("X-RateLimit-Daily-Remaining", "?")
            set_name = products[0].get("setName") if products else str(i)
            print(f"  {len(products)} products fetched. From set: {set_name} | Credits used: {credits_used} | Remaining: {credits_remaining}")
            yield i, products
            time.sleep(2)


    ###################


    def get_past_price_history_test2(self, set_nums):

        for set_num in set_nums:

            params = {
            "language": "english",
            "includeHistory": "true",
            "days": 180,
            "setId": set_num,
            "fetchAllInSet": "true",
            "minPrice": 0.60}
            
            response = requests.get(f"{self.base_url}/cards", headers=self.headers, params=params )
            print(response.status_code)
            
            data = response.json()
            # cards = data.get("data",[])
            # yield set_num, cards

            if response.status_code == 429:
                retry_after = data.get("retryAfter", 60)
                print(f"  Rate limited — waiting {retry_after}s")
                time.sleep(retry_after)
                response = requests.get(f"{self.base_url}/cards", headers=self.headers, params=params)
                data = response.json()

            if response.status_code == 403:
                print(f"  BLOCKED: {data.get('message')} — stopping")
                return

            if response.status_code != 200:
                print(f"  API ERROR {response.status_code}: {data}")
                yield set_num, []
                time.sleep(2)
                continue

            cards = data.get("data", [])
            credits_used = response.headers.get("X-API-Calls-Consumed", "?")
            credits_remaining = response.headers.get("X-RateLimit-Daily-Remaining", "?")
            set_name = cards[0].get("setName") if cards else str(set_num)
            print(f"  Set {set_name}: {len(cards)} cards | Credits used: {credits_used} | Remaining: {credits_remaining}")
            yield set_num, cards
            time.sleep(2)

    def get_past_price_history_test_sealed(self, set_nums):
            
        for set_num in set_nums:
            params = {
            "language": "english",
            "includeHistory": "true",
            "days": 180,
            "setId": set_num}

            response = requests.get(f"{self.base_url}/sealed-products", headers=self.headers, params = params)
            data = response.json()


            if response.status_code == 429:
                retry_after = data.get("retryAfter", 60)
                print(f"  Rate limited — waiting {retry_after}s")
                time.sleep(retry_after)
                response = requests.get(f"{self.base_url}/sealed-products", headers=self.headers, params=params)
                data = response.json()

            if response.status_code == 403:
                print(f"  BLOCKED: {data.get('message')} — stopping")
                return

            if response.status_code != 200:
                print(f"  API ERROR {response.status_code}: {data}")
                yield set_num, []
                time.sleep(2)
                continue

            products = data.get("data", [])
            credits_used = response.headers.get("X-API-Calls-Consumed", "?")
            credits_remaining = response.headers.get("X-RateLimit-Daily-Remaining", "?")
            set_name = products[0].get("setName") if products else str(set_num)
            print(f"  Set {set_name}: {len(products)} products | Credits used: {credits_used} | Remaining: {credits_remaining}")
            yield set_num, products
            time.sleep(2)

