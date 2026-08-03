from utils.database import get_set_ids_to_search, get_set_name_to_id_pair, insert_into_cards_table, insert_into_price_history_table
from utils.api import get_card_data
from utils.transformations import filter_cards
import csv

# CREATING CARDS AND PRICE_HISTORY TABLES IN DB
# fetches all cards from each set using tcg_numeric_id from sets table
# filters out cards with no tcgPlayerId (code cards, unreleased sets)
# filters out cards with market price below $0.99
# cleans card names that have card number appended (e.g. "Pikachu - 037/128" → "Pikachu")

# NOTES:
# set_name from /cards endpoint always matches set_name in sets table (verified)
# set_name_to_id dict bridges card's setName to the set_id slug for FK
# snapshot_date is UTC date when script runs
# price_updated_on is UTC date from API's prices.lastUpdated field


def save_skipped_to_csv(skipped, filename="skipped_cards.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["reason", "name", "setName", "rarity", "market_price", "card_id"])
        writer.writeheader()
        writer.writerows(skipped)
    print(f"Saved {len(skipped)} skipped cards to {filename}")

def save_zero_card_sets_to_csv(zero_card_sets, filename="zero_card_sets.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["tcg_numeric_id"])
        for s in zero_card_sets:
            writer.writerow([s])
    print(f"Saved {len(zero_card_sets)} zero-card sets to {filename}")


set_num = get_set_ids_to_search()
set_name_to_id = get_set_name_to_id_pair()
all_skipped = []
zero_card_sets = []
total_sets = len(set_num)
completed = 0



for set_id, cards in get_card_data(set_num):
    completed += 1
    if not cards:
        zero_card_sets.append(set_id)
        continue
    valid_cards, skipped = filter_cards(cards, set_name_to_id)
    all_skipped.extend(skipped)
    insert_into_cards_table(valid_cards, set_name_to_id)
    insert_into_price_history_table(valid_cards)
    print(f"[{completed}/{total_sets}] Set {set_id}: {len(valid_cards)} inserted, {len(skipped)} skipped")

save_skipped_to_csv(all_skipped)
save_zero_card_sets_to_csv(zero_card_sets)