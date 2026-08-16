from utils.api import PokemonTrackerAPI
from utils.transformations import filter_sets
from utils.database import insert_into_sets_table
from datetime import datetime, timezone
api = PokemonTrackerAPI()
print(f"Sets Table Run started: {datetime.now(timezone.utc)}")


#api call to /sets endpoint. get each sets data (1 call)
sets_data = api.api_get_sets_data()

#removing the sets with no cards in them? (unreleased or error)
set_data_to_insert, set_num = filter_sets(sets_data)

#inserting to db, just the remaining data after removing unreleased or error sets
sets_inserted = insert_into_sets_table(set_data_to_insert)

print(f"\n=== SETS RUN COMPLETE - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} ===")
# print(f"Sets inserted/updated: {len(set_data_to_insert)}")
print(f"Sets checked: {len(set_data_to_insert)} | New sets inserted: {sets_inserted}")