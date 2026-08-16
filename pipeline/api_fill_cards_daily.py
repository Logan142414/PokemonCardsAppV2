from utils.database import get_set_ids_to_search, get_set_name_to_id_pair, insert_into_cards_table, insert_into_price_history_table, save_skipped_cards_to_table, save_zero_card_sets_to_table
from utils.api import PokemonTrackerAPI
from utils.transformations import filter_cards
from datetime import datetime, timezone
api = PokemonTrackerAPI()
print(f"Cards Daily Price Run started: {datetime.now(timezone.utc)}")


set_num = get_set_ids_to_search() #get list of set_ids to send to /cards api
set_name_to_id = get_set_name_to_id_pair() #a dict that contains each set slug and set name
all_skipped = []
zero_card_sets = []
total_sets = len(set_num)
completed = 0
total_cards_inserted = 0
total_valid = 0


for set_id, cards in api.api_get_card_data(set_num):
    completed += 1
    if not cards:
        zero_card_sets.append(set_id)
        continue
    valid_cards, skipped = filter_cards(cards, set_name_to_id)
    all_skipped.extend(skipped)
    cards_inserted = insert_into_cards_table(valid_cards, set_name_to_id)
    insert_into_price_history_table(valid_cards)
    total_cards_inserted += cards_inserted
    total_valid += len(valid_cards)
    print(f"[{completed}/{total_sets}] Set {set_id}: {cards_inserted} new, {len(valid_cards) - cards_inserted} already existed, {len(skipped)} filtered out")

    
save_skipped_cards_to_table(all_skipped)
save_zero_card_sets_to_table(zero_card_sets)

print(f"\n=== DAILY CARDS RUN COMPLETE - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} ===")
print(f"Sets processed: {completed}/{total_sets}")
print(f"Zero card sets: {len(zero_card_sets)}")
print(f"Total skipped cards: {len(all_skipped)}")
print(f"New cards inserted: {total_cards_inserted} | Already existed: {total_valid - total_cards_inserted}")







# def save_skipped_to_csv(skipped, filename="skipped_cards.csv"):
#     date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
#     for row in skipped:
#         row["snapshot_date"] = date_str
    
#     file_exists = os.path.exists(filename)
#     with open(filename, "a", newline="") as f:
#         writer = csv.DictWriter(f, fieldnames=["snapshot_date", "reason", "name", "setName", "rarity", "market_price", "card_id"])
#         if not file_exists:
#             writer.writeheader()
#         writer.writerows(skipped)
#     print(f"Saved {len(skipped)} skipped cards to {filename}")

# def save_zero_card_sets_to_csv(zero_card_sets, filename="zero_card_sets.csv"):
#     date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
#     file_exists = os.path.exists(filename)
#     with open(filename, "a", newline="") as f:
#         writer = csv.writer(f)
#         if not file_exists:
#             writer.writerow(["snapshot_date", "tcg_numeric_id"])
#         for s in zero_card_sets:
#             writer.writerow([date_str, s])
#     print(f"Saved {len(zero_card_sets)} zero-card sets to {filename}")

# save_skipped_to_csv(all_skipped)
# save_zero_card_sets_to_csv(zero_card_sets)