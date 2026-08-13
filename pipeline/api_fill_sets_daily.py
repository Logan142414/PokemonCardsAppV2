from utils.api import PokemonTrackerAPI
from utils.transformations import filter_sets
from utils.database import insert_into_sets_table
api = PokemonTrackerAPI()

# CREATING SET TABLE IN DB
# only looking at english cards, set limit to 500 since default is 100.
# want set id, set name, release date of set, era the set is from, card count of set, tcg_numeric_id to send to /card endpoint

# NOTES:
# 3 sets had no cards in them
# A handful of sets did not have release date - manually added these
# A handful of sets did not have correct era listed either - manually add some of these

#api call to /sets endpoint. get each sets data (1 call)
sets_data = api.api_get_sets_data()

#removing the sets with no cards in them? (unreleased or error)
set_data_to_insert, set_num = filter_sets(sets_data)

#inserting to db, just the remaining data after removing unreleased or error sets
insert_into_sets_table(set_data_to_insert)