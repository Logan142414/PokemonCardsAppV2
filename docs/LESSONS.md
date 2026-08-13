# Lessons & Topics — Pokémon Price Tracker
 
A running log of things learned, things to learn more about, and notes on the software engineering + data workflow behind this project.
 
---
 
## Topics I am exploring
 
### API Calls & Data Extraction
 
- Making GET requests using the `requests` library — passing headers for auth (Bearer token), and params for filtering/sorting
- POST requests would use JSON body instead of params
- Parsing API responses: figuring out if the top level is a dict or list, then peeling back layers using `.keys()`, `type()`, and `[0]` to navigate nested structures
- Handling pagination, rate limits (429), and auth errors (403)
- Using `yield` to create generator functions — lets you process one set at a time instead of loading everything into memory
- Tracking API credit usage via response headers (`X-API-Calls-Consumed`, `X-RateLimit-Daily-Remaining`)


### ETL Pipeline
 
- **ETL = Extract → Transform → Load** (what this project does)
  - Extract: API calls to get card/set/sealed product data
  - Transform: cleaning card names, filtering by price, extracting specific fields (image URL, date, market price), handling nulls
  - Load: inserting into Supabase PostgreSQL
- **ELT = Extract → Load → Transform** — load raw data first, clean it after
- Field extraction counts as transformation (e.g. pulling `data["prices"]["market"]` or `data["priceHistory"]["conditions"]["Near Mint"]["history"]`)
- Date formatting: passing UTC datetime strings to a `date` column in Postgres — the DB handles the conversion automatically

### Data Cleaning
 
- Card names sometimes include card numbers appended (e.g. `Pikachu - 037/128` or `Karen - XY177a`)
- Current `clean_card_name()` handles the `name - number/total` pattern — more patterns likely exist
- Strategy: fix the function permanently for daily runs, then do a one-time SQL UPDATE to patch existing rows
- `ON CONFLICT (card_id) DO UPDATE SET card_name = EXCLUDED.card_name` — lets you re-run the insert and only update the name column

### Database (PostgreSQL / psycopg2)
 
- `psycopg2` is the Python library for connecting to PostgreSQL databases
- Supabase is a managed PostgreSQL database in the cloud — the connection string is all you need
- Other databases have similar libraries: `pymysql` for MySQL, `sqlite3` is built into Python for SQLite
- Key psycopg2 pattern: `get_connection()` → `cursor()` → `execute()` → `commit()` → `close()`
- Schema concepts: primary keys, foreign keys, composite keys (e.g. `card_id + snapshot_date`), data types (`text`, `numeric`, `date`)
- Upsert patterns:
  - `ON CONFLICT DO NOTHING` — skip duplicates silently
  - `ON CONFLICT DO UPDATE SET` — update specific columns on conflict
  - `cursor.rowcount` — tells you if a row was actually inserted (1) or skipped (0)
- FK violations: inserting a row that references a non-existent row in a parent table — causes `psycopg2.errors.ForeignKeyViolation`
- Always insert parent table first (e.g. `cards` before `price_history`, `sealed_products` before `sealed_price_history`)

### Pipeline Design Patterns
 
- Separating concerns into `utils/api.py`, `utils/database.py`, `utils/transformations.py`
- Tracking progress with counters and logs (`[completed/total]`)
- Saving skipped records to CSV for later review
- Using `completed_sets.txt` to resume a multi-day run without re-spending credits
- `time.sleep()` between API calls to avoid rate limiting
- Try/except for FK violations — log the problem card and continue instead of crashing
---
 
 
### SQL
 
This is important both for examining the data I have and for writing the analytics queries in the final app.
 
- Basic queries: `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, `LIMIT`
- Aggregations: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
- Joins: combining tables — `INNER JOIN`, `LEFT JOIN`
  - Example: join `cards` + `sets` + `price_history` to get full card info with prices
- Window functions: powerful for analytics
  - `ROW_NUMBER()`, `RANK()`, `LAG()`, `LEAD()`
  - Rolling averages, % change over time
- CTEs (Common Table Expressions): cleaner way to write complex queries using `WITH`
- Indexes: speed up queries on large tables — worth adding on `card_id`, `snapshot_date`
### Automation (Running Daily Scripts)
 
- **Cron jobs** — Mac/Linux built-in scheduler, runs scripts at set times
  - Example: `0 8 * * * python -m pipeline.daily_cards` runs every day at 8am
- **GitHub Actions** — free CI/CD tool, can run scripts on a schedule
  - Good for cloud-based automation without needing your Mac to be on
- **Logging** — write logs to files instead of just printing to terminal, so you can review what happened even if you weren't watching
- **Alerting** — get notified if a script fails (email, Slack, etc.)
### Data Analytics
 
- Working with time series price data
- Calculating price changes over different windows (7d, 14d, 30d)
- Identifying trends — which cards are rising/falling
- Spotting anomalies — unusual price spikes or drops
- Tools: SQL for querying, Pandas for manipulation, Plotly/Matplotlib for visualization
- These can be done in SQL, Python, or both depending on complexity

---
 
## Front End (To Learn)
 
This is the area I know least about. Notes so far:
 
### Options
 
- **Streamlit** — Python only, handles almost everything, minimal customization, good for quick dashboards
- **Flask / FastAPI** — Python backend that serves data via an API to a separate frontend
- **Next.js / React** — JavaScript, full control over design and behavior, steeper learning curve
- The "stack" matters: Streamlit is all-in-one. A real web app is usually a backend API + separate frontend

### Running Locally vs Deploying
 
- **Local**: just run the script, view in browser at `localhost`
- **Deploy options**: Vercel (Next.js), Railway, Render, Heroku — these host your app so others can access it
- Deployment also means thinking about environment variables, secrets management, and build processes

### Things I Don't Yet Understand Well
 
- How frontend and backend communicate (REST APIs, fetch calls)
- CSS / styling fundamentals
- Component-based design (React)
- How routing works in web apps
- Authentication / login systems
- When to use server-side vs client-side rendering
---
 
## Things I'm Aware of but Not Diving Into Yet
 
- **Auth / login** — restricting access to the app
- **Error logging tools** — Sentry, Datadog for tracking errors in production
- **Security** — protecting API keys, SQL injection prevention, etc.
- **Testing** — unit tests, integration tests for pipeline functions
- **Docker** — containerizing the app so it runs the same anywhere

