import psycopg2
from utils.database import get_connection



########### SIMPLE STARTING FETCH

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""SELECT * FROM sets""")
rows = cursor.fetchall
for row in rows:
    print(row)

cursor.close()
conn.close()



#######################


conn = get_connection()
cursor = conn.cursor()

cursor.execute("""SELECT DISTINCT snapshot_date FROM price_history """)
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()


#######################
# GROUP BY - essentially splits into sub tables based on what your grouping by. In this case a diff table for each unique snapshot_date there is

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""SELECT snapshot_date, COUNT(*)
                FROM price_history
               GROUP BY snapshot_date """)
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()

