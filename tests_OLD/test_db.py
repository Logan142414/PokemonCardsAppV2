from database import get_connection, read_table
##takes connection string and opens live connection to db
# def get_connection():
#     return psycopg2.connect(os.getenv("DATABASE_URL"))


#check the connection 
try:
    conn = get_connection()
    print("✅ Connected to Supabase successfully!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")


#read the "Sets" table
try:
    sets_table = read_table("Sets")
    print(sets_table)

except Exception as e:
    print(f"Unable to access the table: {e}")


#read the "Cards" table
try:
    sets_table = read_table("Cards")
    print(sets_table)

except Exception as e:
    print(f"Unable to access the table: {e}")
