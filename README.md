# Poke-Crawler

A simple tool that helps crawl some Pokémon Generation 1 data from [pokemondb.net](https://pokemondb.net/), including:
- `151 Pokémon` in Generation 1 (Red, Blue, Yellow)
- `156 Moves` in Generation 1 
- `Type chart` in Generation 1 (still keeping the "mistakes" that are said to be corrected in later generations)
- `Evolution chain` data in Generation 1 (**by level up only**)

#### Configuration
Check the files in `crawler/spiders/gen_1/` to configure what you want or update the code according to any changes on `pokemondb.net`.

#### Re-crawl data
I crawled the above data into the `/res/gen_1/` folder. However, in case you want to re-crawl them, check out the `run.sh` script.

Or you can just run this script by:
```
./run.sh
```