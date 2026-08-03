# need to look at every set using /sets endpoint - to fill the sets table
#tcgplayerid from /sets endpoint (set_id) , name from /sets endpoint (set_name),  releaseDate from /sets endpoint(release date), 
#  series from /sets endpoint (era), cardCount from /sets endpoint (card_count)


import http.client
import json
import urllib.parse
from dotenv import load_dotenv
import os
from utils.database import get_connection
from datetime import datetime
import requests

load_dotenv()
PokemonK = os.getenv("Pokemon_K")
PokemonK_URL=os.getenv("Pokemon_K_URL")

def fetch_all_sets():

    all_sets = []
    offset = 0
    limit = 500  # max allowed
    
    while True:
        params = {
            "language": "english",
            "limit": limit,
            "offset": offset,
            "sortBy": "releaseDate",
            "sortOrder": "desc"
        }
        

        headers = {"Authorization": f"Bearer {PokemonK}"}
        url = f'{PokemonK_URL}/api/v2/sets'
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        sets = data.get("data", [])
        all_sets.extend(sets)
        
        if not data["metadata"]["hasMore"]:
            break
            
        offset += limit
        
    return all_sets


def insert_sets(sets):
    db = get_connection()
    cursor = db.cursor()
    
    for s in sets:
        cursor.execute("""
            INSERT INTO sets (set_id, set_name, release_date, era, card_count, tcg_numeric_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (set_id) DO UPDATE SET tcg_numeric_id = EXCLUDED.tcg_numeric_id
        """, (
            s["tcgPlayerId"],
            s["name"],
            s.get("releaseDate"),
            s.get("series"),
            s.get("cardCount"),
            s.get("tcgPlayerNumericId")  # ← new field
        ))
    
    db.commit()
    cursor.close()
    db.close()
    print(f"Inserted {len(sets)} sets")


if __name__ == "__main__":
    sets = fetch_all_sets()
    print(f"Fetched {len(sets)} sets")
    insert_sets(sets)



params = {
            "language": "english",
            "sortBy": "releaseDate",
            "sortOrder": "desc"
        }
        

headers = {"Authorization": f"Bearer {PokemonK}"}
url = f'{PokemonK_URL}/api/v2/sets'
response = requests.get(url, headers=headers, params=params)
data = response.json()