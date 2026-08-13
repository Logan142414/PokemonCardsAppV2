from utils.api import PokemonTrackerAPI
from utils.database import get_set_name_to_id_pair, insert_into_price_history_table_sealed, get_set_ids_to_search, insert_into_sealed_product_table
from utils.transformations import filter_sealed_products
from datetime import datetime, timezone
import csv
import os
api = PokemonTrackerAPI()


def save_skipped_sealed_to_csv(skipped, filename="skipped_products.csv"):
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for row in skipped:
        row["snapshot_date"] = date_str
    
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["snapshot_date", "reason", "name", "setName", "price", "product_id"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(skipped)
    print(f"Saved {len(skipped)} skipped products to {filename}")

def save_zero_product_sets_to_csv(zero_product_sets, filename="zero_product_sets.csv"):
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["snapshot_date", "tcg_numeric_id"])
        for s in zero_product_sets:
            writer.writerow([date_str, s])
    print(f"Saved {len(zero_product_sets)} zero-product sets to {filename}")


set_nums = get_set_ids_to_search()
set_name_to_id = get_set_name_to_id_pair()
all_skipped = []
zero_product_sets = []
total_sets = len(set_nums)
completed = 0

for set_id, products in api.api_get_sealed_data(set_nums):
    completed += 1
    if not products:
        zero_product_sets.append(set_id)
        continue
    valid_products, skipped = filter_sealed_products(products, set_name_to_id)
    all_skipped.extend(skipped)
    insert_into_sealed_product_table(valid_products, set_name_to_id)
    insert_into_price_history_table_sealed(valid_products)
    print(f"[{completed}/{total_sets}] Set {set_id}: {len(products)} inserted, {len(all_skipped)} skipped")

save_skipped_sealed_to_csv(all_skipped)
save_zero_product_sets_to_csv(zero_product_sets)

