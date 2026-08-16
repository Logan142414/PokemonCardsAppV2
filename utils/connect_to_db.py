import psycopg2
from utils.database import get_connection
import pandas as pd
from utils.transformations import clean_card_name



########### SIMPLE STARTING FETCH

# conn = get_connection()
# cursor = conn.cursor()

# cursor.execute("""SELECT * FROM sets""")
# rows = cursor.fetchall
# for row in rows:
#     print(row)

# cursor.close()
# conn.close()



#######################
#simple row print

# conn = get_connection()
# cursor = conn.cursor()

# cursor.execute("""SELECT DISTINCT card_name, card_number FROM cards """)
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# cursor.close()
# conn.close()


#OR to send to Dataframe

conn = get_connection()
df = pd.read_sql("SELECT DISTINCT card_name, card_number FROM cards", conn)
conn.close()
df['card_name_cleaned'] = df.apply(lambda row: clean_card_name(row['card_name'], row['card_number']), axis=1)

# print(df.shape)
# len(df)
print(df.shape)
print(df.head(20))
print(df["card_name"].nunique())
print(df[df["card_name"].str.contains(" - ", na=False)])
df.to_csv("card_names_UpdateTest2.csv", index=False)



#######################
# GROUP BY - essentially splits into sub tables based on what your grouping by. In this case a diff table for each unique snapshot_date there is

# conn = get_connection()
# cursor = conn.cursor()

# cursor.execute("""SELECT snapshot_date, COUNT(*)
#                 FROM price_history
#                GROUP BY snapshot_date """)
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# cursor.close()
# conn.close()

#############
