# Development Log


## July 22, 2026

- Created the repo in GitHub
- Created a first draft of architecture diagram (whimsical.com)
    - Linear top-down flow: Pokemon Data Source (API or Web Scraper) → Daily Scheduler → Python ETL Pipeline (Extract → Transform → Load) → Supabase DB (Historical Prices) → SQL Queries / Statistics / Visualizations → Streamlit Dashboard / UI → User
    - Noted the daily run would cover most English Pokemon set cards (15k+)
    - Daily scheduler to run at a set time — cron or GitHub Actions TBD
    - Supabase chosen because it is managed PostgreSQL in the cloud
    - Streamlit chosen as a simple, sharable web page option - noted as a potential future replacement with Next.js
- Noted that the daily run would cover ~6,500 cards (130 sets × top 50 cards per set, sorted by price)
- Wrote the README.md
- Set up Supabase


## July 23, 2026

- Created a first draft of a schema diagram (whimsical.com)
    - Three tables: price_history, sets, cards
    - price_history: card_id, date, price, PSA 8, PSA 9, PSA 10, gem rate
    - sets: set_id, set name, release date, era
    - cards: card_id, card name, image (TBD)
    - Key decisions:
        - price_nm named explicitly for near mint to avoid ambiguity
        - gem_rate stored in price_history since it comes from the API daily, even though it moves slowly
        - Storing raw daily snapshots only — price changes (7d, 14d, 30d) computed at query time, not stored as columns. Keeps the schema stable and lets new metrics be added without touching the pipeline.
        - Schema is intentionally flexible pending API selection — fields like image_url, gem_rate, and price_psa8 may be adjusted depending on what the API actually returns


- Looking into https://www.pokemonpricetracker.com/ - "price_history" table (will run daily job)
  - $9.99/month API tier — 20,000 credits/day, 60 requests/minute
  - Need to verify: bulk endpoint availability and what card ID format they use (must match card_id in cards table)
  - Signing up for free tier first to test before purchasing

- Looking into https://github.com/PokemonTCG/pokemon-tcg-data/tree/master - one time pull for "sets" and "cards" tables (update when new set releases)

## July 25, 2026

- Finalized data types for both tables (text, date, int2)
- Created `sets` and `cards` tables in Supabase with correct schema, data types, and FK relationship
- Started using `psycopg2` library in Python to connect to Supabase, read tables, and insert data
- Wrote `database.py` with reusable functions: `get_connection()`, `read_table()`, `insert_set_data()`, `insert_card_data()`, `insert_card_rarity()`
- Wrote `load_sets.py` and `load_cards.py` to populate both tables from the GitHub JSON data
- Filled tables: 174 sets, 20,444 cards
- Confirmed data quality - no nulls or empty strings across all columns, no duplicate card_ids
- Added `rarity` column to cards table — will use this to filter which cards get daily price scraping. Plan to exclude Common, Uncommon, NULL, and Rare (~12,550 cards), leaving ~7,400 cards worth tracking (as of July 2026)


## July 26, 2026

- Starting to compare different api options as  https://www.pokemonpricetracker.com/ doesn't give graded card prices
    - ttps://www.pokemonpricetracker.com/ ($9.99 a month for ungraded prices, sealed product prices. $100 to get graded numbers)
    - https://www.pricecharting.com/ ($49.99 a month to get ungraded prices, sealed product prices, and graded numbers)
    - https://tcgapi.dev/ ($9.99 a month to get... $20/mo and $50/mo plans as well...)
    - https://justtcg.com/ ($20 a month... or even more expensive plans)
    - https://silphcoanalytics.xyz/docs/api/getting-started?

## Aug 1, 2026

- Switched fully to pokemonpricetracker.com as the single data source for all card metadata and pricing
- Removed data populated from the GitHub JSON repo — maintaining two sources with mismatched IDs added unnecessary complexity
- Spent time exploring the API: tested set, card, and pricing endpoints to understand response structure, available fields, and rate limits
- Discovered the API has two rate limits: 20,000 credits/day and 150 requests per 5 minutes (undocumented)
- Took an ELT approach for initial data exploration - loaded raw data into Supabase first, then explored with SQL to understand what needed cleaning
- Hit API rate limit during initial full cards load — added `time.sleep(2.5)` and retry logic with exponential backoff
- Sets table findings: 3 sets had card_count = 0, some sets missing release dates, several "Other" era sets needed era corrections, some sets (McDonald's promos, Trick or Trade, Battle Academy) produce no trackable cards
- Restructured project into `pipeline/` and `utils/` folders for clean separation of concerns

## Aug 2, 2026

- Re-filled sets table using new pipeline script (`api_fill_sets_FINAL.py`) with cleaned logic
- Added `tcg_numeric_id` column to sets table — required for the /cards endpoint which expects numeric GroupId, not the slug
- Confirmed that `name` from /sets endpoint always matches `setName` from /cards endpoint across all 214 sets (0 mismatches) — validates the FK lookup approach
- Added `minPrice=0.99` filter to cards API calls to reduce credit usage by ~50%
- Built `utils/transformations.py` with `clean_card_name()` to handle cards where API appends card number to name (e.g. "Pikachu - 037/128" → "Pikachu")
- Updated README to reflect current architecture and previous version history
