# Need to go set by set.... get every card that isnt rarity (blank , blank , blank?)
# call the /cards endpoint. This will fill the cards table and the price history table

#Fill the cards table with:
# then from each card get the tcgPlayerId from /cards endpoint(card_id_), tcgPlayerId from the /sets endpoint (set_id),
#  name from /cards endpoint (card_name), cardNumber from /cards endpoint (card_number),  imageCdnUrl400 from /cards endpoint (image), rarity from /cards endpint (rarity)

#Fill the price history table with:
#tcgPlayerId from /cards endpoint(card_id), time when api call is made... (snapshot_date),  market from the /cards endpoint (market_price), lastUpdated from /cards endpoint (price_updated_on)


import http.client
import json
import urllib.parse
from dotenv import load_dotenv
import os
from utils.database import get_connection
from datetime import datetime, timezone
import csv
import time

load_dotenv()
PokemonK = os.getenv("Pokemon_K")

# Rarities to EXCLUDE (not worth tracking)
# EXCLUDE_RARITIES = {
#     "Common", "Uncommon", "Rare", None
# }

def fetch_cards_for_set(tcg_numeric_id, retries=3):
    conn = http.client.HTTPSConnection("www.pokemonpricetracker.com")
    headers = {"Authorization": f"Bearer {PokemonK}"}
    
    params = urllib.parse.urlencode({
        "setId": tcg_numeric_id,
        "fetchAllInSet": "true",
        "sortBy": "price",
        "sortOrder": "desc",
        "language": "english"
    })
    
    conn.request("GET", f"/api/v2/cards?{params}", headers=headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    if res.status == 429:
        error_message = data.get('error', '')
        
        # Daily limit exhausted - no point retrying
        if 'daily' in error_message.lower() or 'credit' in error_message.lower():
            print(f"  Daily credit limit reached - stopping run")
            return None  # signal to stop
        
        # Minute rate limit - retry after waiting
        if retries == 0:
            print(f"  Max retries reached, skipping set {tcg_numeric_id}")
            return []
        retry_after = data.get("retryAfter", 60)
        print(f"  Rate limited — waiting {retry_after}s (retries left: {retries})")
        time.sleep(retry_after)
        return fetch_cards_for_set(tcg_numeric_id, retries=retries-1)

    if res.status != 200:
        print(f"  API ERROR {res.status}: {data}")
        return []

    credits_used = res.getheader("X-API-Calls-Consumed", "?")
    credits_remaining = res.getheader("X-RateLimit-Daily-Remaining", "?")
    print(f"  API returned {len(data.get('data', []))} cards | Credits used: {credits_used} | Remaining: {credits_remaining}")
    return data.get("data", [])


def insert_cards_and_prices(cards, snapshot_date, set_name_to_id):
    db = get_connection()
    cursor = db.cursor()

    cards_inserted = 0
    prices_inserted = 0
    no_match_cards = []

    for card in cards:

        if cards.index(card) == 0:
            print(f"  Sample setName: '{card.get('setName')}' → lookup result: '{set_name_to_id.get(card.get('setName'))}'")

        rarity = card.get("rarity")
        
        # Skip excluded rarities
        # if rarity in EXCLUDE_RARITIES:
        #     continue

        card_id = card.get("tcgPlayerId")

        if not card_id:
            print(f"NO CARD ID: {card.get('name')} | setName: {card.get('setName')}")
            no_match_cards.append({
                "name": card.get("name"),
                "setName": card.get("setName"),
                "rarity": rarity,
                "market_price": card.get("prices", {}).get("market"),
                "card_id": "NO_ID"
            })
            continue

        market_price = card.get("prices", {}).get("market")
        price_updated_on_raw = card.get("prices", {}).get("lastUpdated")
        set_id = set_name_to_id.get(card.get("setName"))


        
        # Log and skip if no set match
        if not set_id:
            print(f"NO SET MATCH: {card.get('name')} | setName: {card.get('setName')}")
            no_match_cards.append({
                "name": card.get("name"),
                "setName": card.get("setName"),
                "rarity": rarity,
                "market_price": market_price,
                "card_id": card_id
            })
            continue


        # Skip if no price
        if not market_price:
            continue

        # Convert price_updated_on to date
        price_updated_on = datetime.fromisoformat(
            price_updated_on_raw.replace("Z", "+00:00")
        ).date() if price_updated_on_raw else None

        # Insert into cards table
        cursor.execute("""
            INSERT INTO cards (card_id, set_id, card_name, card_number, image_front_url, rarity)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (card_id) DO NOTHING
        """, (
            card_id,
            set_id,
            card.get("name"),
            card.get("cardNumber"),
            card.get("imageCdnUrl400"),
            rarity
        ))
        cards_inserted += 1

        # Insert into price_history table
        cursor.execute("""
            INSERT INTO price_history (card_id, snapshot_date, market_price, price_updated_on)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (card_id, snapshot_date) DO NOTHING
        """, (
            card_id,
            snapshot_date,
            market_price,
            price_updated_on
        ))
        prices_inserted += 1

    db.commit()
    cursor.close()
    db.close()
    print(f"  Cards inserted: {cards_inserted} | Prices inserted: {prices_inserted} | Skipped (no match/price): {len(no_match_cards)}")


    if no_match_cards:
        file_exists = os.path.exists("no_set_match_cards.csv")
        with open("no_set_match_cards.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "setName", "rarity", "market_price", "card_id"])
            if not file_exists:
                writer.writeheader()
            writer.writerows(no_match_cards)

    return cards_inserted, prices_inserted 

    

if __name__ == "__main__":
    snapshot_date = datetime.now(timezone.utc).date()
    
    db = get_connection()
    cursor = db.cursor()
    
     # Get both set_id slug AND numeric id
    cursor.execute("SELECT set_id, set_name, tcg_numeric_id FROM sets")
    rows = cursor.fetchall()
    
    # Build name -> slug lookup for FK matching
    set_name_to_id = {row[1]: row[0] for row in rows}
    
    # Build list of (slug, numeric_id) tuples for API calls
    sets_to_process = []
    for row in rows:
        if row[2] is not None:
            sets_to_process.append((row[0], row[2]))
        else:
            print(f"SKIPPING - no numeric id: {row[0]} | {row[1]}")
    
    cursor.close()
    db.close()

    total_cards = 0
    total_prices = 0

    for set_id, tcg_numeric_id in sets_to_process:
        print(f"Processing set: {set_id} (numeric: {tcg_numeric_id})")
        cards = fetch_cards_for_set(tcg_numeric_id)  # ← use numeric id
        if cards is None:
            print(f"\n=== DAILY CREDIT LIMIT REACHED — stopping ===")
            break 
        
        c, p = insert_cards_and_prices(cards, snapshot_date, set_name_to_id)
        total_cards += c
        total_prices += p
        time.sleep(5) 

    print(f"\n=== DONE ===")
    print(f"Total cards inserted: {total_cards}")
    print(f"Total prices inserted: {total_prices}")