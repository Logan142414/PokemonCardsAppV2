import psycopg2 #Python talk to a Postgres database
from dotenv import load_dotenv
import os
from utils.transformations import clean_card_name, classify_product_type
from datetime import datetime, timezone

load_dotenv()


#CONNECT WITH SUPABASE DB FUNCTION
def get_connection():
    """Test connection to supabase db. Takes connection string and opens live connection to db"""
    return psycopg2.connect(os.getenv("DATABASE_URL"))


#READ TABLE IN SUPABASE DB FUNCTION
def read_table(table_name):
    """Connects to db and then reads full table based on what is inputed in function call"""
    con = get_connection()
    cur = con.cursor()

    cur.execute(f"select * from {table_name}")
    rows = cur.fetchall()
    for r in rows:
        print(r)

    cur.close()
    con.close()


##########


# get the set ids that I will feed into the /cards endpoint 
def get_set_ids_to_search():
    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        "SELECT tcg_numeric_id FROM sets")

    result = cursor.fetchall()
    set_num = [i[0] for i in result]
    cursor.close()
    db.close()
    print(f"Retrevied {len(set_num)} set ids")
    return set_num

#make a dict to contain set slug and set name
def get_set_name_to_id_pair():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT set_name, set_id FROM sets")
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return {row[0]: row[1] for row in rows}

def get_set_id_to_set_name_pair():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT tcg_numeric_id, set_name FROM sets")
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return {row[0]: row[1] for row in rows}



def get_product_ids_to_search():
    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        "SELECT product_id FROM sealed_product")

    result = cursor.fetchall()
    product_num = [i[0] for i in result]
    cursor.close()
    db.close()
    print(f"Retrevied {len(product_num)} product_ids")
    return product_num


#insert data into cards table
def insert_into_cards_table(cards_from_each_set,set_name_to_id):
    db = get_connection()
    cursor = db.cursor()
    inserted = 0

    for i in cards_from_each_set:
        cursor.execute("""INSERT INTO cards (card_id, set_id, card_name, card_number, image_front_url, rarity)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (card_id) DO NOTHING""",
                        (i.get("tcgPlayerId"),
                        set_name_to_id.get(i.get("setName")),
                        clean_card_name(i.get("name")),
                        i.get("cardNumber"),
                        i.get("imageCdnUrl400"),
                        i.get("rarity")
                            
                    ))
        if cursor.rowcount == 1:
            inserted += 1

    db.commit()
    cursor.close()
    db.close()
    return inserted 
    # print(f" {inserted} new cards inserted, {len(cards_from_each_set) - inserted} already existed")


#insert data into price history (for first time)
def insert_into_price_history_table(cards_from_each_set):
    snapshot_date = datetime.now(timezone.utc).date()

    db = get_connection()
    cursor = db.cursor()

    for i in cards_from_each_set:
        cursor.execute("""INSERT INTO price_history (card_id, snapshot_date, market_price, price_updated_on)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (card_id, snapshot_date) DO NOTHING""",
                        (i.get("tcgPlayerId"),
                        snapshot_date,
                        i.get("prices", {}).get("market"),
                        i.get("prices", {}).get("lastUpdated")
                            
                    ))

    db.commit()
    cursor.close()
    db.close()



def insert_into_sets_table(sets_to_insert):
    db = get_connection()
    cursor = db.cursor()
    inserted = 0

    for s in sets_to_insert:
        cursor.execute("""
                INSERT INTO sets (set_id, set_name, release_date, era, card_count, tcg_numeric_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (set_id) DO NOTHING
            """, (
                s["tcgPlayerId"],
                s["name"],
                s.get("releaseDate"),
                s.get("series"),
                s.get("cardCount"),
                s.get("tcgPlayerNumericId")
            ))
        if cursor.rowcount == 1:
            inserted += 1

    db.commit()
    cursor.close()
    db.close()
    return inserted 
    # print(f"Sets checked: {len(sets_to_insert)} | New/updated: {inserted}")



def insert_into_sealed_product_table(products_to_insert, set_name_to_id):
    db = get_connection()
    cursor = db.cursor()
    inserted = 0

    for s in products_to_insert:
        cursor.execute("""
                INSERT INTO sealed_products (product_id, product_name, set_id, image_url, product_type)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (product_id) DO NOTHING
            """, (
                s["tcgPlayerId"],
                s.get("name"),
                set_name_to_id.get(s.get("setName")), 
                s.get("imageCdnUrl400"), 
                classify_product_type(s.get("name"))
            ))
        inserted += cursor.rowcount

    db.commit()
    cursor.close()
    db.close()
    return inserted 
    # print(f"  {inserted} new products inserted, {len(products_to_insert) - inserted} already existed")



def insert_into_price_history_table_sealed(products_to_insert):
    db = get_connection()
    cursor = db.cursor()
    snapshot_date = datetime.now(timezone.utc).date()

    for s in products_to_insert:
        cursor.execute("""
                INSERT INTO sealed_price_history (product_id, snapshot_date, market_price, price_updated_on)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (product_id, snapshot_date) DO NOTHING
                """, (
                s.get("tcgPlayerId"),
                snapshot_date,
                s.get("unopenedPrice"),
                s.get("lastScrapedAt")
                ))

    db.commit()
    cursor.close()
    db.close()



def insert_price_history_past_180days(cards_from_each_set):
    db = get_connection()
    cursor = db.cursor()
    fk_violations = []

    for x in cards_from_each_set:
        card_id = x["tcgPlayerId"]
        history = x["priceHistory"]["conditions"]["Near Mint"]["history"]
        for i in history:
            # print(card_id, i["date"], i["market"], i['date'])
            
            try:
                cursor.execute("""
                        INSERT INTO price_history (card_id, snapshot_date, market_price, price_updated_on)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (card_id, snapshot_date) DO NOTHING
                    """, (
                        card_id,
                        i["date"],
                        i["market"], 
                        i['date']
                    ))
            
            except Exception as e:
                    db.rollback()
                    fk_violations.append({"card_id": card_id, "name": x.get("name")})
                    break  # stop trying other dates for this card
            
    db.commit()
    cursor.close()
    db.close()
    
    if fk_violations:
        print(f"  FK violations (card not in cards table): {len(fk_violations)}")
        for v in fk_violations:
            print(f"    - {v['name']} ({v['card_id']})")



def insert_price_history_past_180days_sealed(products_from_each_set):
    db = get_connection()
    cursor = db.cursor()
    fk_violations = []
    
    for product in products_from_each_set:
        product_id = product.get("tcgPlayerId")
        history = product.get("priceHistory", [])
        
        for i in history:
            try:
                cursor.execute("""
                        INSERT INTO sealed_price_history (product_id, snapshot_date, market_price, price_updated_on)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (product_id, snapshot_date) DO NOTHING
                    """, (
                        product_id,
                        i["date"],
                        i["unopenedPrice"],
                        i['date']
                    ))
            except Exception as e:
                    db.rollback()
                    fk_violations.append({"product_id": product_id, "name": product.get("name")})
                    break  
    db.commit()
    cursor.close()
    db.close()
    
    if fk_violations:
        print(f"  FK violations ( product not available in product table): {len(fk_violations)}")
        for v in fk_violations:
            print(f"    - {v['name']} ({v['product_id']})")


#####################################################################

def save_skipped_cards_to_table(skipped):
    conn = get_connection()
    cursor = conn.cursor()
    snapshot_date = datetime.now(timezone.utc).date()

    for row in skipped:
        cursor.execute("""INSERT INTO skipped_cards (date, reason, card_name, set_name, market_price, card_id)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                       (snapshot_date,
                        row.get("reason"),
                        row.get("name"),
                        row.get("setName"),
                        row.get("market_price"),
                        row.get("card_id")))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Saved {len(skipped)} skipped cards to DB")


def save_zero_card_sets_to_table(zero_card_sets):
    conn = get_connection()
    cursor = conn.cursor()
    snapshot_date = datetime.now(timezone.utc).date()
    tcg_id_to_name = get_set_id_to_set_name_pair()

    for set_id in zero_card_sets:
        cursor.execute("""INSERT INTO zero_cards_added_sets (date, set_id, set_name)
                       VALUES (%s, %s, %s)""",
                       (snapshot_date, set_id, tcg_id_to_name.get(set_id)))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Saved {len(zero_card_sets)} zero-card sets to DB")


def save_zero_product_sets_to_table(zero_product_sets):
    conn = get_connection()
    cursor = conn.cursor()
    snapshot_date = datetime.now(timezone.utc).date()
    tcg_id_to_name = get_set_id_to_set_name_pair()

    for set_id in zero_product_sets:
        cursor.execute("""INSERT INTO zero_products_added_sets (date, set_id, set_name)
                       VALUES (%s, %s, %s)""",
                       (snapshot_date, set_id, tcg_id_to_name.get(set_id)))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Saved {len(zero_product_sets)} zero-product sets to DB")


def save_skipped_sealed_to_table(skipped):
    conn = get_connection()
    cursor = conn.cursor()
    snapshot_date = datetime.now(timezone.utc).date()

    for row in skipped:
        cursor.execute("""INSERT INTO skipped_products (date, reason, product_name, set_name, sealed_price, product_id)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                       (snapshot_date,
                        row.get("reason"),
                        row.get("name"),
                        row.get("setName"),
                        row.get("price"),
                        row.get("product_id")))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Saved {len(skipped)} skipped products to DB")


#####################################################################

# CLEAR DATA FROM THE SETS TABLE
def clear_sets_table():
    con = get_connection()
    cur = con.cursor()
    cur.execute("TRUNCATE TABLE sets CASCADE")
    con.commit()
    cur.close()
    con.close()

#CLEAR THE DATA FROM THE CARDS TABLE
def clear_cards_table():
    con = get_connection()
    cur = con.cursor()
    cur.execute("TRUNCATE TABLE cards CASCADE")
    con.commit()
    cur.close()
    con.close()
