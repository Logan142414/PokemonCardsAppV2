import psycopg2 #Python talk to a Postgres database
from dotenv import load_dotenv
import os
import json

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


#WRITE THE DATA TO SETS TABLE
def insert_set_data():
    """Take json file and insert the data into the sets table"""
    con = get_connection()
    cur = con.cursor()

    with open('data/pokemon-tcg-data-master/sets/en.json','r') as sets_file:
        data =json.load(sets_file)

    for set in data:
        # print(set['id'],set["name"],set["releaseDate"],set["series"],set["images"]["logo"])
        cur.execute("""INSERT INTO sets (set_id, set_name, release_date, era, logo_url)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (set_id) DO NOTHING""",

                    (set["id"],
                    set["name"],
                    set["releaseDate"],
                    set["series"],
                    set["images"]["logo"]
                    ))
        
    con.commit()

    cur.close()
    con.close()

    
#WRITE THE DATA TO CARDS TABLE

def insert_card_data():
    """Take json file and insert the data into the cards table"""

    con = get_connection()
    cur = con.cursor()

    printedTotals = {}
    with open('data/pokemon-tcg-data-master/sets/en.json','r') as sets_file:
        data =json.load(sets_file)

    for set in data:
        printedTotals[set["id"]] = set["printedTotal"]


    list_of_set_files = os.listdir('data/pokemon-tcg-data-master/cards/en/')

    full_data = []
    for set in list_of_set_files:
        with open(f'data/pokemon-tcg-data-master/cards/en/{set}','r') as cards_file:
            data=json.load(cards_file)
            full_data.append(data)

    # print(data)
    for set in full_data:
        for card in set:
            set_id = card["id"].split("-")[0]
            printed_total = printedTotals[set_id]
            
            # print(card["id"],set_id,card["name"],card["number"],printed_total, card["images"]["small"])
            cur.execute("""INSERT INTO cards (card_id, set_id, card_name, card_number, printed_total, image_front_url)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (card_id) DO NOTHING""",

                        (card["id"],
                        set_id,
                        card["name"],
                        card["number"],
                        printed_total, 
                        card["images"]["small"]
                        ))
            
    con.commit()

    cur.close()
    con.close()


# ADD RARITY DATA TO CARDS TABLE
def insert_card_rarity():
    """Take json file and insert the data into the cards table"""

    con = get_connection()
    cur = con.cursor()

    list_of_set_files = os.listdir('data/pokemon-tcg-data-master/cards/en/')

    full_data = []
    for set in list_of_set_files:
        with open(f'data/pokemon-tcg-data-master/cards/en/{set}','r') as cards_file:
            data=json.load(cards_file)
            full_data.append(data)

    # print(data)
    for set in full_data:
        for card in set:
            
            # print(card["rarity"])
            cur.execute("""UPDATE cards 
               SET rarity = %s 
               WHERE card_id = %s""",

                (card.get("rarity"), 
                card["id"]))
            
            
    con.commit()

    cur.close()
    con.close()
