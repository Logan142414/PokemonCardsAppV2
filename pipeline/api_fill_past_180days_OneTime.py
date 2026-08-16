from utils.database import get_set_ids_to_search, insert_price_history_past_180days, get_set_name_to_id_pair
from utils.api import PokemonTrackerAPI
from utils.transformations import filter_cards, filter_cards_with_history
import csv
from datetime import datetime, timezone
import os
import json

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

all_skipped = []
all_skipped_history = []

for set_id, cards in api.get_past_price_history_test2(remaining):
    if not cards:
        print(f"  No cards for set {set_id} - marking complete")
        with open(completed_past_180_day_sets, "a") as f:
            f.write(f"{set_id}\n")
        continue
    # valid_cards, skipped = filter_cards(cards, set_name_to_id) 
    # valid_cards, skipped_history = filter_cards_with_history(valid_cards) 
    valid_cards, skipped = filter_cards(cards, set_name_to_id)
    all_skipped.extend(skipped)
    valid_cards, skipped_history = filter_cards_with_history(valid_cards)
    all_skipped_history.extend(skipped_history)

    print(
        f"""
        Set {set_id}
        Total API cards: {len(cards)}
        Skipped basic filters: {len(skipped)}
        Skipped no history: {len(skipped_history)}
        Inserted: {len(valid_cards)}
        """
    )

    insert_price_history_past_180days(valid_cards)
    with open(completed_past_180_day_sets, "a") as f:
        f.write(f"{set_id}\n")


    with open("skipped_basic_filters.json", "w") as f:
        json.dump(all_skipped, f, indent=2)

    with open("skipped_history_cards.json", "w") as f:  
        json.dump(all_skipped_history, f, indent=2)


