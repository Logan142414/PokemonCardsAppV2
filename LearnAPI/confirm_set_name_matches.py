from dotenv import load_dotenv, find_dotenv
import os 
import requests
import time


load_dotenv()
PokemonK = os.getenv("Pokemon_K")
PokemonK_URL = os.getenv("Pokemon_K_URL")


############################################### Get the tcgPlayerNumericId from /sets endpoint. Save in "set_num"
# only looking at english cards, set limit to 500 since default is 100, 
params = {
            "language": "english",
            "sortBy": "releaseDate",
            "sortOrder": "desc",
            "limit": 500
        }
        
headers = {"Authorization": f"Bearer {PokemonK}"}
url = f'{PokemonK_URL}/api/v2/sets'
response = requests.get(url, headers=headers, params=params)
data = response.json()

set_names = []
set_num = []
for i in data["data"]:
    if i["cardCount"] == 0:
        print(f"SKIPPING - no cards: {i['tcgPlayerId']}")
        continue
    print(f"set_id: {i["tcgPlayerId"]}, set_name: {i["name"]}, release_date: {i.get('releaseDate')}, era: {i["series"]}, card_count: {i["cardCount"]}" )
    set_names.append(i["name"])
    set_num.append(i["tcgPlayerNumericId"])

# print(data) # print the whole api call result
# print(data["metadata"])

#now set_names is a list of all the "name" field that comes from the /set endpoint 
# print(set_names)
# print(set_num)



###################################################### Do a test of getting 1 cards data from each set (217 total)
headers = {"Authorization": f"Bearer {PokemonK}"}
one_card_each_set = []
set_names_from_cards = []
for i in set_num:

    params = {"language": "english",
            "limit": 1,
            "sortBy": "price",
            "setId": i}
    
    url = f'{PokemonK_URL}/api/v2/cards'
    response = requests.get(url, headers = headers, params = params)
    data = response.json()
    cards = data.get("data", [])
    if cards:
        one_card_each_set.append(cards[0])
        set_names_from_cards.append(cards[0]["setName"])
    time.sleep(1)

print(one_card_each_set)




#################### compare "set_names" list created from the /sets endpoint (name) 
# with the "set_names_from_cards" list created from the /cards endpoint (setName)
 
#length comparison
print(len(set_names))         
print(len(set_names_from_cards))


#mismatch check
mismatches = []
for set_name, c_name in zip(set_names, set_names_from_cards):
    if set_name == c_name:
        continue
    else:
        mismatches.append((set_name, c_name))

print(mismatches)
    

