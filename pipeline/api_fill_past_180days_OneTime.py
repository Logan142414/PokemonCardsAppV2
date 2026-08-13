from utils.database import get_set_ids_to_search, insert_price_history_past_180days, get_set_name_to_id_pair
from utils.api import PokemonTrackerAPI
from utils.transformations import filter_cards, filter_cards_with_history
import csv
from datetime import datetime, timezone
import os
api = PokemonTrackerAPI()

completed_past_180_day_sets = "completed_sets.txt"

if os.path.exists(completed_past_180_day_sets):
    with open (completed_past_180_day_sets) as f:
        completed = set(f.read().splitlines())

else:
    completed = set()


set_nums = get_set_ids_to_search() #get list of set_ids to send to /cards api
set_name_to_id = get_set_name_to_id_pair()

remaining = []
for i in set_nums:
    if str(i) not in completed: 
        remaining.append(i)
    else:
        print(f"Skipping {i} - already done")


for set_id, cards in api.get_past_price_history_test2(remaining):
    if not cards:
        print(f"  No cards for set {set_id} - marking complete")
        with open(completed_past_180_day_sets, "a") as f:
            f.write(f"{set_id}\n")
        continue
    valid_cards, skipped = filter_cards(cards, set_name_to_id) 
    valid_cards, skipped_history = filter_cards_with_history(valid_cards) 
    print(f"Inserting history for set {set_id}, {len(valid_cards)} cards")
    insert_price_history_past_180days(valid_cards)
    with open(completed_past_180_day_sets, "a") as f:
        f.write(f"{set_id}\n")


