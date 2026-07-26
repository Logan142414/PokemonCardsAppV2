# Filling "sets" db table with the set data I need. Comes from a github repo.
# Will only need to run everytime a new set comes about (normally every 3 months or so)
# Source (One file called “en.json”): https://github.com/PokemonTCG/pokemon-tcg-data/tree/master/sets

from database import insert_set_data

insert_set_data()