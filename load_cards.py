# Filling "sets" db table with the set data I need. Comes from a github repo.
# Will only need to run everytime a new set comes about (normally every 3 months or so)
# Source (One file for each set): https://github.com/PokemonTCG/pokemon-tcg-data/tree/master/cards/en 

from database import insert_card_data, insert_card_rarity

# insert_card_data()
insert_card_rarity()