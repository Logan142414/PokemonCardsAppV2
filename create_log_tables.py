import psycopg2
from utils.database import get_connection
# conn = psycopg2.connect(os.getenv("DATABASE_URL"))

def create_skipped_cards_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE skipped_cards ( 
                   date date,
                   reason text,
                   card_name text, 
                   set_name text, 
                   market_price numeric,
                   card_id text
                   )""")
    conn.commit()
    conn.close()
    cursor.close()


def create_skipped_products_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE skipped_products ( 
                   date date,
                   reason text,
                   product_name text, 
                   set_name text, 
                   sealed_price numeric,
                   product_id text
                   )""")

    conn.commit()
    conn.close()
    cursor.close()


def create_zero_cards_added_sets_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE  zero_cards_added_sets ( 
                   date date,
                   set_id text
                   )""")
    
    conn.commit()
    conn.close()
    cursor.close()


def create_zero_products_added_sets_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE  zero_products_added_sets( 
                   date date,
                   set_id text
                   )""")

    conn.commit()
    conn.close()
    cursor.close()

create_skipped_cards_table()
create_skipped_products_table()
create_zero_cards_added_sets_table()
create_zero_products_added_sets_table()