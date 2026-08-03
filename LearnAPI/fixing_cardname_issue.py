test_names = [
    "Mega Darkrai ex - 120/084",      # should strip → "Mega Darkrai ex"
    "Ho-Oh",                           # should keep → "Ho-Oh"
    "Porygon-Z - 33/65",                       # should keep → "Porygon-Z"
    "Jangmo-o",                        # should keep → "Jangmo-o"
    "Tapu Koko-GX",                    # should keep → "Tapu Koko-GX"
    "Pikachu - 037/128",               # should strip → "Pikachu"
    "Type: Null",                      # should keep → "Type: Null"
    "Kommo-o - 096/131",               # should strip → "Kommo-o"
]

for card_name in test_names:
    if card_name and " - " in card_name:
        parts = card_name.split(" - ")
        if "/" in parts[-1]:
            card_name = parts[0].strip()
    print(card_name)