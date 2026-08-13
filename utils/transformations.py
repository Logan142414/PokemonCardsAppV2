
def clean_card_name(name):
    if name and " - " in name:
        parts = name.split(" - ")
        if "/" in parts[-1]:
            return parts[0].strip()
    return name


def filter_sets(sets_data):
    set_data_to_insert = []
    set_num = []
    for i in sets_data:
        if i["cardCount"] == 0:
            print(f"SKIPPING - no cards: {i['tcgPlayerId']}")
            continue
        print(f"set_id: {i["tcgPlayerId"]}, set_name: {i["name"]}, release_date: {i.get('releaseDate')}, era: {i["series"]}, card_count: {i["cardCount"]}, tcg_numeric_id: {i["tcgPlayerNumericId"]}  " )
        set_num.append(i["tcgPlayerNumericId"])
        set_data_to_insert.append(i)
    return set_data_to_insert, set_num


def filter_cards(cards_from_each_set, set_name_to_id):
    valid_cards = []
    skipped = []
    
    for i in cards_from_each_set:
        card_id = i.get("tcgPlayerId")
        if not card_id:
            print(f"  SKIP (no_card_id): {i.get('name')} | {i.get('setName')}")
            skipped.append({
                "reason": "no_card_id",
                "name": i.get("name"),
                "setName": i.get("setName"),
                "rarity": i.get("rarity"),
                "market_price": i.get("prices", {}).get("market"),
                "card_id": "NO_ID"
            })
            continue
        
        set_id = set_name_to_id.get(i.get("setName"))
        if not set_id:
            print(f"  SKIP (no_set_match): {i.get('name')} | {i.get('setName')}")
            skipped.append({
                "reason": "no_set_match",
                "name": i.get("name"),
                "setName": i.get("setName"),
                "rarity": i.get("rarity"),
                "market_price": i.get("prices", {}).get("market"),
                "card_id": card_id
            })
            continue
        
        market_price = i.get("prices", {}).get("market")
        if not market_price:
            print(f"  SKIP (no_price): {i.get('name')} | {i.get('setName')}")
            skipped.append({
                "reason": "no_price",
                "name": i.get("name"),
                "setName": i.get("setName"),
                "rarity": i.get("rarity"),
                "market_price": None,
                "card_id": card_id
            })
            continue
        
        valid_cards.append(i)
    
    return valid_cards, skipped


def filter_sealed_products(products, set_name_to_id):
    valid_products = []
    skipped = []
    
    for i in products:
        product_id = i.get("tcgPlayerId")
        if not product_id:
            print(f"  SKIP (no_product_id): {i.get('name')} | {i.get('setName')}")
            skipped.append({
                "reason": "no_product_id",
                "name": i.get("name"),
                "setName": i.get("setName"),
                "price": i.get("unopenedPrice"),
                "product_id": "NO_ID"
            })
            continue
        
        set_id = set_name_to_id.get(i.get("setName"))
        if not set_id:
            print(f"  SKIP (no_set_match): {i.get('name')} | {i.get('setName')}")
            skipped.append({
                "reason": "no_set_match",
                "name": i.get("name"),
                "setName": i.get("setName"),
                "price": i.get("unopenedPrice"),
                "product_id": product_id
            })
            continue
        
        valid_products.append(i)
    
    return valid_products, skipped


def filter_cards_with_history(cards_from_each_set):
    valid_cards = []
    skipped = []
    
    for x in cards_from_each_set:
        nm_history = x.get("priceHistory", {}).get("conditions", {}).get("Near Mint", {}).get("history")
        if not nm_history:
            print(f"  SKIP (no NM history): {x.get('name')}")
            skipped.append(x.get("name"))
            continue
        valid_cards.append(x)
    
    return valid_cards, skipped

def filter_products_with_history(products):
    valid_products = []
    skipped = []
    
    for x in products:
        history = x.get("priceHistory", [])
        if not history:
            print(f"  SKIP (no price history): {x.get('name')}")
            skipped.append(x.get("name"))
            continue
        valid_products.append(x)
    
    return valid_products, skipped
