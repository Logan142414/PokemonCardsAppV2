# Manual Set Corrections

## Release Date Corrections
Sets where the API returned NULL for release_date. Dates sourced from https://www.tcgplayer.com/content/article/Every-Pok%C3%A9mon-TCG-Set-in-Order-Newest-to-Oldest/02f9330b-d44a-48d3-9162-f4ce1909f0f6/

| set_id | set_name | release_date |
|--------|----------|--------------|
| pop-series-1 | POP Series 1 | 2004-09-01 |
| pop-series-2 | POP Series 2 | 2005-08-01 |
| pop-series-3 | POP Series 3 | 2006-04-01 |
| pop-series-4 | POP Series 4 | 2006-08-01 |
| pop-series-5 | POP Series 5 | 2007-03-01 |
| pop-series-6 | POP Series 6 | 2007-09-01 |
| pop-series-7 | POP Series 7 | 2008-03-01 |
| pop-series-8 | POP Series 8 | 2008-09-01 |
| pop-series-9 | POP Series 9 | 2009-03-01 |
| ex-trainer-kit-1-latias-and-latios | EX Trainer Kit 1: Latias & Latios | 2004-06-01 |
| ex-trainer-kit-2-plusle-and-minun | EX Trainer Kit 2: Plusle & Minun | 2005-03-15 |
| nintendo-promos | Nintendo Promos | 2003-09-01 |
| pikachu-world-collection-promos | Pikachu World Collection Promos | 2010-11-01 |
| first-partner-pack | First Partner Pack | 2001-07-31 |

## No Date Available (left as NULL)
- `alternate-art-promos` — no official release date found
- `professor-program-promos` — no official release date found
- `blister-exclusives` — no official release date found
- `miscellaneous-cards-and-products` — no official release date found

<!-- -- POP Series
UPDATE sets SET release_date = '2004-09-01' WHERE set_id = 'pop-series-1';
UPDATE sets SET release_date = '2005-08-01' WHERE set_id = 'pop-series-2';
UPDATE sets SET release_date = '2006-04-01' WHERE set_id = 'pop-series-3';
UPDATE sets SET release_date = '2006-08-01' WHERE set_id = 'pop-series-4';
UPDATE sets SET release_date = '2007-03-01' WHERE set_id = 'pop-series-5';
UPDATE sets SET release_date = '2007-09-01' WHERE set_id = 'pop-series-6';
UPDATE sets SET release_date = '2008-03-01' WHERE set_id = 'pop-series-7';
UPDATE sets SET release_date = '2008-09-01' WHERE set_id = 'pop-series-8';
UPDATE sets SET release_date = '2009-03-01' WHERE set_id = 'pop-series-9';

-- Trainer Kits
UPDATE sets SET release_date = '2004-06-01' WHERE set_id = 'ex-trainer-kit-1-latias-and-latios';
UPDATE sets SET release_date = '2005-03-15' WHERE set_id = 'ex-trainer-kit-2-plusle-and-minun';

-- Promos
UPDATE sets SET release_date = '2003-09-01' WHERE set_id = 'nintendo-promos';
UPDATE sets SET release_date = '2010-11-01' WHERE set_id = 'pikachu-world-collection-promos';

-- Other
UPDATE sets SET release_date = '2001-07-31' WHERE set_id = 'first-partner-pack'; -->


## Era Corrections
Sets where the API returned "Other" but belong to a specific era. Dates sourced from (https://www.tcgplayer.com/content/article/Every-Pok%C3%A9mon-TCG-Set-in-Order-Newest-to-Oldest/02f9330b-d44a-48d3-9162-f4ce1909f0f6/)


| set_id | set_name | corrected_era |
|--------|----------|---------------|
| black-and-white | Black and White | Black & White |
| emerging-powers | Emerging Powers | Black & White |
| noble-victories | Noble Victories | Black & White |
| next-destinies | Next Destinies | Black & White |
| dark-explorers | Dark Explorers | Black & White |
| boundaries-crossed | Boundaries Crossed | Black & White |
| plasma-storm | Plasma Storm | Black & White |
| plasma-freeze | Plasma Freeze | Black & White |
| plasma-blast | Plasma Blast | Black & White |
| legendary-treasures | Legendary Treasures | Black & White |
| bw-trainer-kit-excadrill-and-zoroark | BW Trainer Kit: Excadrill & Zoroark | Black & White |
| kalos-starter-set | Kalos Starter Set | XY |
| double-crisis | Double Crisis | XY |
| generations | Generations | XY |
| generations-radiant-collection | Generations: Radiant Collection | XY |
| xy-trainer-kit-sylveon-and-noivern | XY Trainer Kit: Sylveon & Noivern | XY |
| xy-trainer-kit-bisharp-and-wigglytuff | XY Trainer Kit: Bisharp & Wigglytuff | XY |
| xy-trainer-kit-latias-and-latios | XY Trainer Kit: Latias & Latios | XY |
| xy-trainer-kit-pikachu-libre-and-suicune | XY Trainer Kit: Pikachu Libre & Suicune | XY |
| shining-legends | Shining Legends | Sun & Moon |
| detective-pikachu | Detective Pikachu | Sun & Moon |
| hidden-fates | Hidden Fates | Sun & Moon |
| hidden-fates-shiny-vault | Hidden Fates: Shiny Vault | Sun & Moon |
| sm-trainer-kit-lycanroc-and-alolan-raichu | SM Trainer Kit: Lycanroc & Alolan Raichu | Sun & Moon |
| sm-trainer-kit-alolan-sandslash-and-al | SM Trainer Kit: Alolan Sandslash & Alolan Ninetales | Sun & Moon |
| celebrations | Celebrations | Sword & Shield |
| celebrations-classic-collection | Celebrations: Classic Collection | Sword & Shield |
| shining-fates | Shining Fates | Sword & Shield |
| shining-fates-shiny-vault | Shining Fates: Shiny Vault | Sword & Shield |
| champions-path | Champion's Path | Sword & Shield |
| pokemon-go | Pokemon GO | Sword & Shield |
| sve-scarlet-and-violet-energies | SVE: Scarlet & Violet Energies | Scarlet & Violet |
| hgss-trainer-kit-gyarados-and-raichu | HGSS Trainer Kit: Gyarados & Raichu | HeartGold & SoulSilver |
| diamond-and-pearl | Diamond and Pearl | Diamond & Pearl |



REMAINING AS OTHER:
trading-card-game-classic
rumble
southern-islands
jumbo-cards
world-championship-decks
prize-pack-series-cards
league-and-championship-cards
deck-exclusives
blister-exclusives
miscellaneous-cards-and-products
battle-academy, battle-academy-2022, battle-academy-2024
trick-or-trade-booster-bundle, trick-or-trade-booster-bundle-2023, trick-or-trade-booster-bundle-2024
my-first-battle
first-partner-pack, first-partner-collection-2026
legendary-treasures-radiant-collection


<!-- 
UPDATE sets SET era = 'Black & White' WHERE set_id IN (
    'black-and-white', 'emerging-powers', 'noble-victories', 'next-destinies',
    'dark-explorers', 'boundaries-crossed', 'plasma-storm', 'plasma-freeze',
    'plasma-blast', 'legendary-treasures', 'bw-trainer-kit-excadrill-and-zoroark'
);

UPDATE sets SET era = 'XY' WHERE set_id IN (
    'kalos-starter-set', 'double-crisis', 'generations', 'generations-radiant-collection',
    'xy-trainer-kit-sylveon-and-noivern', 'xy-trainer-kit-bisharp-and-wigglytuff',
    'xy-trainer-kit-latias-and-latios', 'xy-trainer-kit-pikachu-libre-and-suicune'
);

UPDATE sets SET era = 'Sun & Moon' WHERE set_id IN (
    'shining-legends', 'detective-pikachu', 'hidden-fates', 'hidden-fates-shiny-vault',
    'sm-trainer-kit-lycanroc-and-alolan-raichu', 'sm-trainer-kit-alolan-sandslash-and-al'
);

UPDATE sets SET era = 'Sword & Shield' WHERE set_id IN (
    'celebrations', 'celebrations-classic-collection', 'shining-fates',
    'shining-fates-shiny-vault', 'champions-path', 'pokemon-go'
);

UPDATE sets SET era = 'Scarlet & Violet' WHERE set_id IN (
    'sve-scarlet-and-violet-energies'
);

UPDATE sets SET era = 'HeartGold & SoulSilver' WHERE set_id IN (
    'hgss-trainer-kit-gyarados-and-raichu'
);

UPDATE sets SET era = 'Diamond & Pearl' WHERE set_id IN (
    'diamond-and-pearl'
); -->