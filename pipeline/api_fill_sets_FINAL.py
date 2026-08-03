from utils.api import fetch_sets
from utils.transformations import filter_sets
from utils.database import insert_sets

# CREATING SET TABLE IN DB
# only looking at english cards, set limit to 500 since default is 100.
# want set id, set name, release date of set, era the set is from, card count of set, tcg_numeric_id to send to /card endpoint

# NOTES:
# 3 sets had no cards in them
# A handful of sets did not have release date - manually added these
# A handful of sets did not have correct era listed either - manually add some of these



data = fetch_sets()
sets_to_insert, set_num = filter_sets(data)
insert_sets(sets_to_insert)