from utils.database import get_set_ids_to_search, insert_price_history_past_180days_sealed, get_set_name_to_id_pair
from utils.api import PokemonTrackerAPI
from utils.transformations import filter_sealed_products, filter_products_with_history
import csv
from datetime import datetime, timezone
import os
api = PokemonTrackerAPI()

set_nums = get_set_ids_to_search()
set_name_to_id = get_set_name_to_id_pair()

# first, have logic so I keep track of all the sets I have already processed in a txt file.
# 1) check if the txt file already exists. If yes, grab the contents and put into a "set". If no, it will be an empty "set" for now.
# 2) make a list called remaining - using the setids, one by one see if the completed "set" includes the setid value.


completed_past_180_day_sets_SEALED_PROD = "completed_sets_SEALED.txt"
if os.path.exists(completed_past_180_day_sets_SEALED_PROD):
    with open(completed_past_180_day_sets_SEALED_PROD, "r") as f:
        completed = set(f.read().splitlines())
        print(completed)
else:
    completed = set()

remaining = []
for i in set_nums:
    if str(i) not in completed:
        remaining.append(i)
    else:
        print(f"Skipping {i} - already done")
    

# Then, run the api call that puts in one "set_num" at a time per api call. Then inserts into db

for set_id, products in api.get_past_price_history_test_sealed(remaining):
    if not products:
        print(f"  No products for set {set_id} - marking complete")
        with open(completed_past_180_day_sets_SEALED_PROD, "a") as f:
            f.write(f"{set_id}\n")
        continue

    # valid_cards, skipped = filter_cards(cards, set_name_to_id) 
    # valid_cards, skipped_history = filter_cards_with_history(valid_cards) 
    # print(f"Inserting history for set {set_id}, {len(valid_cards)} cards")
    # insert_price_history_past_180days(valid_cards)
    # with open(completed_past_180_day_sets, "a") as f:
    #     f.write(f"{set_id}\n")

    valid_products, skipped = filter_sealed_products(products, set_name_to_id)
    valid_products, skipped_history = filter_products_with_history(valid_products)
    print(f"Inserting history for set {set_id}, {len(valid_products)} products")
    insert_price_history_past_180days_sealed(valid_products)
    with open(completed_past_180_day_sets_SEALED_PROD, "a") as f:
        f.write(f"{set_id}\n")
    











#The main thing you use a set for is exactly what you're doing here — 
# checking if something is already in a collection. 
# if x not in my_set is much faster than if x not in my_list for large collections.


# for example:

# I have a LIST of set_nums [22223, 5554, 23233]...
# But I want to see if anything in my txt file is in that list. Cause then I can remove from the "to-do" sets which to start was full set_nums list