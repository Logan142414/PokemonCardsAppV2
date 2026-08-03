import psycopg2 #Python talk to a Postgres database
from dotenv import load_dotenv
import os
from utils.transformations import clean_card_name
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

#make a dict to contain set slug and set name that will be 
def get_set_name_to_id_pair():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT set_name, set_id FROM sets")
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return {row[0]: row[1] for row in rows}



#insert data into cards table
def insert_into_cards_table(cards_from_each_set,set_name_to_id):
    db = get_connection()
    cursor = db.cursor()

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
    db.commit()
    cursor.close()
    db.close()


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



def insert_sets(sets_to_insert):
    db = get_connection()
    cursor = db.cursor()

    for s in sets_to_insert:
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
                s.get("tcgPlayerNumericId")
            ))

    db.commit()
    cursor.close()
    db.close()
    print(f"Inserted {len(sets_to_insert)} sets")



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
