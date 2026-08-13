import requests
from dotenv import load_dotenv
import os

load_dotenv()

Pokemon_K = os.getenv("Pokemon_K")
Pokemon_K_URL = os.getenv("Pokemon_K_URL")

# print(url)
def get_past_price_history_test():
    headers = {"Authorization": f"Bearer {Pokemon_K}"}
    url = f"{Pokemon_K_URL}/cards"

    params = {
    "language": "english",
    "includeHistory": "true",
    "days": 180,
    "setId": 23821,
    "limit": 1}
    
    response = requests.get(url, headers=headers, params=params )
    print(response.status_code)
    data = response.json()
    cards = data.get("data",[])
    for x in cards:
        card_id = x["tcgPlayerId"]
    for i in cards[0]["priceHistory"]["conditions"]["Near Mint"]["history"]:
        print(card_id, i["date"], i["market"], i["date"])


# r = get_past_price_history_test()
# r

# I need data["tcgPlayerId"]   - this is card_id
# I need data["priceHistory"]["conditions"]["Near Mint"]["history"] 
# ^ 180 of these: ["date"] - snapshot_date 
# ^ 180 of these: ["date"] - price_udpated_on
# ^ 180 of these ["market"] - market_price



def get_past_price_history_test2():
    headers = {"Authorization": f"Bearer {Pokemon_K}"}
    url = f"{Pokemon_K_URL}/cards"

    set_nums = [17674,3172]
    for set_num in set_nums:

        params = {
        "language": "english",
        "includeHistory": "true",
        "days": 180,
        "setId": set_num}
        
        response = requests.get(url, headers=headers, params=params )
        print(response.status_code)
        data = response.json()
        cards = data.get("data",[])
        
        for x in cards:
            card_id = x["tcgPlayerId"]
            history = x["priceHistory"]["conditions"]["Near Mint"]["history"]
            for i in history:
                print(card_id, i["date"], i["market"], i['date'])


r = get_past_price_history_test2()
r
