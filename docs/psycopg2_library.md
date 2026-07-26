## Important notes for how to use psycopg2 library

- `conn = psycopg2.connect()` — opens a connection to the database
- `cur = conn.cursor()` — creates a cursor, which is what actually executes queries (read or write)
- `cur.execute()` — runs a SQL statement (SELECT, INSERT, UPDATE, etc.)
- `conn.commit()` — permanently saves any writes to the database. Without this, inserts/updates are lost when the connection closes
- `cur.close()` / `conn.close()` — always call these when done to free up the connection