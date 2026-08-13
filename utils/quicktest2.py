import requests 
from dotenv import load_dotenv
from utils.database import get_set_ids_to_search, get_connection
import os
from utils.quicktest import PokemonTrackerAPI
import psycopg2
from datetime import datetime, timezone


set_nums =get_set_ids_to_search()
set_nums = set_nums[0:2]
print(set_nums) #[24722, 24688]
api = PokemonTrackerAPI()


# db = get_connection()
# cursor = db.cursor()

# enter one set at a time into the api - starting with 24722 , then 24688.
for set_num in set_nums:
    r = api.get_past_price_history_test_sealed(set_num)


 # for each result... now I should to a insert into db!
    db = get_connection()
    cursor = db.cursor()
    snapshot_date = datetime.now(timezone.utc).date()

    cursor.execute(""" INSERT INTO sealed_price_history
                        (product_id, snapshot_date, market_price, price_updated_on)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (product_id, snapshot_date) DO NOTHING """ ,

                        (r.get("tcgPlayerId"),
                        snapshot_date,
                        r.get("unopenedPrice"),
                        r.get("updatedAt")
                        ))

#for sealed table
#  s["tcgPlayerId"],
#                 s.get("name"),
#                 set_name_to_id.get(s.get("setName")), 
#                 s.get("imageCdnUrl400")







    