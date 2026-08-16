from utils.database import get_connection
from utils.transformations import clean_card_name

def backfill_cleaned_names():
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("SELECT card_id, card_name, card_number FROM cards")
    rows = cursor.fetchall()

    updated = 0
    for card_id, card_name, card_number in rows:
        cleaned = clean_card_name(card_name, card_number)
        if cleaned != card_name:
            cursor.execute(
                "UPDATE cards SET card_name = %s WHERE card_id = %s",
                (cleaned, card_id)
            )
            updated += 1

    db.commit()
    cursor.close()
    db.close()
    print(f"Done. {updated} cards updated out of {len(rows)} total.")

if __name__ == "__main__":
    backfill_cleaned_names()