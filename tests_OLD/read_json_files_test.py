import json
import os 
import pandas as pd

#set_id, set_name, release_date, era, image
#read in the set file
# with open('data/pokemon-tcg-data-master/sets/en.json','r') as sets_file:
#     data =json.load(sets_file)
# print(data)
# print(type(data))
# print(data[0])

# for set in data:
#     # print(set['id'],set["name"],set["releaseDate"],set["series"],set["images"]["logo"])
#     cursor.execute("""INSERT INTO sets (set_id, set_name, release_date, era, logo_url)
#                 VALUES (%s, %s, %s, %s, %s,
#                 ON CONFLICT (scraped_date, set_name, card_name) DO NOTHING""",

#                 (set["id"],
#                 set["name"],
#                 set["releaseDate"],
#                 set["series"],
#                 set["images"]["logo"]
#                 ))


# printedTotals = {}
# with open('data/pokemon-tcg-data-master/sets/en.json','r') as sets_file:
#     data =json.load(sets_file)

# for set in data:
#     printedTotals[set["id"]] = set["printedTotal"]

# print(printedTotals)



# list_of_set_files = os.listdir('data/pokemon-tcg-data-master/cards/en/')

# full_data = []
# for set in list_of_set_files:
#     with open(f'data/pokemon-tcg-data-master/cards/en/{set}','r') as cards_file:
#         data=json.load(cards_file)
#         full_data.append(data)

# # print(data)
# rarity_list = []
# for set in full_data:
#     for card in set:
#         # set_id = card["id"].split("-")[0]
#         # printed_total = printedTotals[set_id]
#         # print(card["rarity"],card["id"],set_id,card["name"],card["number"],printed_total, card["images"]["small"])
#         rarity = card.get("rarity")
#         rarity_list.append(rarity)
# # print(rarity_list)


# print(pd.Series(rarity_list).value_counts(dropna=False))
