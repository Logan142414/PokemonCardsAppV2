import re

# def clean_card_name(name):
#     if name and " - " in name:
#         parts = name.split(" - ")
#         if "/" in parts[-1]:
#             return parts[0].strip()
#     return name

def clean_card_name(name, card_number):
    if not name or not card_number:
        return name
    
    base_num = card_number.split('/')[0].lstrip('0') or '0'
    
    # Pattern 1: "Name - CODE remainder" → strip the code if it matches card number
    if ' - ' in name:
        parts = name.split(' - ', 1)
        after_dash = parts[1].strip()
        after_first_token = after_dash.split(' ')[0].split('(')[0].split('[')[0].rstrip(',').strip()
        after_first_lstripped = after_first_token.lstrip('0') or '0'
        
        if (after_first_token == card_number or 
            after_first_lstripped == base_num or
            after_first_token == card_number.split('/')[0]):
            remainder = after_dash[len(after_first_token):].strip()
            name = (parts[0].strip() + ' ' + remainder).strip() if remainder else parts[0].strip()
    
    # Pattern 2: "Name (NUMBER)" where NUMBER matches card number → strip the parens entirely
    paren_match = re.search(r'\s*\((\d+)\)\s*$', name)
    if paren_match:
        num_in_paren = paren_match.group(1).lstrip('0') or '0'
        if num_in_paren == base_num:
            name = name[:paren_match.start()].strip()
    
    # Pattern 3: "Name (NUMBER Text)" → strip just the number, keep the text
    paren_match2 = re.search(r'\((\d+)\s+([^)]+)\)', name)
    if paren_match2:
        num = paren_match2.group(1).lstrip('0') or '0'
        if num == base_num:
            remainder = paren_match2.group(2)
            name = name[:paren_match2.start()] + f'({remainder})' + name[paren_match2.end():]
    
    # Cleanup: fix dangling dash left by Pattern 3 e.g. "(- Holo)" → "(Holo)"
    name = re.sub(r'\(\s*-\s*', '(', name)
    
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
        history = (
            x.get("priceHistory", {})
            .get("conditions", {})
            .get("Near Mint", {})
            .get("history")
        )

        if not history:
            skipped.append({
                "reason": "no_nm_history",
                "card_id": x.get("tcgPlayerId"),
                "name": x.get("name"),
                "set_name": x.get("setName"),
                "market_price": x.get("prices", {}).get("market")
            })
            continue

        valid_cards.append(x)

    return valid_cards, skipped


def filter_products_with_history(products):
    valid_products = []
    skipped = []
    
    for x in products:
        history = x.get("priceHistory", [])

        if not history:
            skipped.append({
                "reason": "no_price_history",
                "product_id": x.get("tcgPlayerId"),
                "name": x.get("name"),
                "set_name": x.get("setName"),
                "price": x.get("unopenedPrice")
            })
            continue

        valid_products.append(x)

    return valid_products, skipped

def classify_product_type(name):
    if not name:
        return 'Other'
    n = name.lower()
    if 'build & battle stadium' in n: return 'Build & Battle Stadium'
    if 'booster box case' in n: return 'Booster Box Case'
    if 'elite trainer box case' in n: return 'ETB Case'
    if 'booster bundle case' in n: return 'Booster Bundle Case'
    if 'booster box' in n: return 'Booster Box'
    if 'pokemon center elite trainer box' in n: return 'Pokemon Center Elite Trainer Box'
    if 'elite trainer box' in n: return 'Elite Trainer Box'
    if 'booster bundle' in n: return 'Booster Bundle'
    if 'booster pack' in n: return 'Booster Pack'
    if 'super premium collection' in n: return 'Super Premium Collection'
    if 'ultra-premium collection' in n: return 'Ultra Premium Collection'
    if 'premium collection' in n: return 'Premium Collection'
    if 'collection box' in n: return 'Collection Box'
    if '3-pack blister case' in n: return '3 Pack Blister Case'
    if '3 pack blister case' in n: return '3 Pack Blister Case'
    if '3 pack blister' in n: return '3 Pack Blister'
    if '3-pack blister' in n: return '3 Pack Blister'
    if 'mini tin display case' in n: return 'Mini Tin Display Case'
    if 'mini tin display' in n: return 'Mini Tin Display'
    if 'mini tin' in n: return 'Mini Tin'
    if 'single pack blister' in n: return 'Single Pack Blister'
    if 'single blister pack' in n: return 'Single Pack Blister'
    if 'build & battle display' in n: return 'Build & Battle Box Display'
    if 'build & battle box' in n: return 'Build & Battle Box'
    if 'league battle deck' in n: return 'League Battle Deck'
    if 'pin collection' in n: return 'Pin Collection'
    if 'tech sticker collection case' in n: return 'Tech Sticker Collection Case'
    if 'tech sticker collection' in n: return 'Tech Sticker Collection'
    if 'binder collection case' in n: return 'Binder Collection Case'
    if 'binder collection' in n: return 'Binder Collection'
    return 'Other'