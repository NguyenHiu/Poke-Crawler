#!/bin/bash

output="./res/gen_1/"
path="./crawler/spiders/gen_1/"
spiders=(
    "fetch_evolution_by_lv_up_gen_1.py"
    "fetch_moves_gen_1.py"
    "fetch_pokemons_gen_1.py"
    "fetch_type_chart_gen_1.py"
)

for spider in "${spiders[@]}"
do
    echo "Running spider: $spider"
    scrapy runspider $path$spider -o $output${spider%.*}.json
    # sleep 100
done