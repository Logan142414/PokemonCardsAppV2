import psycopg2 #Python talk to a Postgres database
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()



#takes connection string and opens live connection to db
def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))




# takes in df which is my scraped data
# starts a connection and then inputs into the card price table
def insert_card_prices(df):
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO card_prices 
                (scraped_date, set_name, card_name, ungraded_price, 
                 grade_9_price, psa_10_price, image_url, deal_value)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (scraped_date, set_name, card_name) DO NOTHING
        """, (
            row["Date"],
            row["Set"],
            row["Card_Name"],
            row["Ungraded_Price"],
            row["Grade_9_Price"],
            row["PSA_10_Price"],
            row["Image_URL"],
            row["Deal_Value"]
        ))

    conn.commit()
    cursor.close()
    conn.close()


#########################
# To grab the data from the db


# loads just todays data from db
def load_latest_prices():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM card_prices
        WHERE scraped_date = (SELECT MAX(scraped_date) FROM card_prices)
    """)
    
    rows = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
    
    cursor.close()
    conn.close()
    
    return pd.DataFrame(rows, columns=cols)

#loads all the data in the card price table
def load_all_history():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM card_prices ORDER BY scraped_date")
    
    rows = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
    
    cursor.close()
    conn.close()
    
    return pd.DataFrame(rows, columns=cols)