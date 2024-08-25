import scrapy
import re
import time


def remove_tags(text):
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)


class FetchMovesSpider(scrapy.Spider):
    name = "fetch_moves"
    allowed_domains = ["pokemondb.net"]

    def __init__(self, start_url="https://pokemondb.net/move/generation/1", *args, **kwargs):
        super(FetchMovesSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]

    def detail_info_parse(self, response, move_name):
        if len(response.css("h2#move-level")) != 0:
            try:
                move_desription = remove_tags(
                    response.css("h2#move-effects")[0]
                    .xpath("..")
                    .css("p")[0]
                    .css("p")
                    .get()
                )
            except:
                move_desription = ""

            try:
                _data = response.css("div.grid-row")[0].css("table tr")
            except:
                yield {}

            try:
                type = _data[0].css("a::text").get().lower()
            except:
                type = ""

            try:
                category = _data[1].css("td::text").get().split(" ")[1].lower()
            except:
                category = ""

            try:
                power = int(_data[2].css("td::text").get())
            except:
                power = 0

            try:
                accuracy = int(_data[3].css("td::text").get())
            except:
                accuracy = 0

            try:
                pp = int(_data[4].css("td::text").get().split(" ")[0])
            except:
                pp = 0

            try:
                max_pp = int(_data[4].css("small::text").get().split(" ")[1][:-1])
            except:
                max_pp = pp

            try:
                make_contact = _data[5].css("td::text").get().lower() == "Yes"
            except:
                make_contact = False

            try:
                introduced = _data[6].css("td::text").get().lower()
            except:
                introduced = ""

            try:
                move_target = [
                    True if "selected" in target.css("::attr(class)").get() else False
                    for target in response.css("div.grid-row")[1].css(
                        "div.move-target  > div.mt-pkmn"
                    )
                ]
            except:
                move_target = []

            _existing_id = set()
            learnt_by_level_up = []
            try:
                for pokemon in response.css("div.infocard-list")[0].css("div.infocard"):
                    _id = pokemon.css("small")[0].css("::text").get().split(" ")[0]
                    if _id in _existing_id:
                        continue
                    _existing_id.add(_id)
                    learnt_by_level_up.append(
                        {
                            "id": _id,
                            "level": int(
                                pokemon.css("small")[-1]
                                .css("::text")
                                .get()
                                .split(" ")[1]
                            ),
                        }
                    )
            except:
                pass

            yield {
                "move_name": move_name,
                "move_desription": move_desription,
                "type": type,
                "category": category,
                "power": power,
                "accuracy": accuracy,
                "pp": pp,
                "max_pp": max_pp,
                "make_contact": make_contact,
                "introduced": introduced,
                "move_target": move_target,
                "learnt_by_level_up": learnt_by_level_up,
            }

    def parse(self, response):
        moves_table = response.css("table#moves")
        moves_list = moves_table.css("tbody tr")
        for move in moves_list:
            _details_page_url = move.css("a.ent-name::attr(href)").get()
            print(f"_details_page_url: {_details_page_url}")
            yield response.follow(
                f"https://pokemondb.net/{_details_page_url}",
                callback=self.detail_info_parse,
                cb_kwargs={
                    "move_name": move.css("a.ent-name::text").get(),
                },
            )
