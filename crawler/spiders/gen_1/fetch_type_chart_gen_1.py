import scrapy
import re
import time


def convert_damage(raw_damage):
    if raw_damage == "0":
        return 0
    elif raw_damage == None:
        return 1
    elif raw_damage == "2":
        return 2
    # elif raw_damage == "½": return 0.5
    return 0.5


class FetchMovesSpider(scrapy.Spider):
    name = "fetch_type_chart"
    allowed_domains = ["pokemondb.net"]

    def __init__(self, start_url="https://pokemondb.net/type/old", *args, **kwargs):
        super(FetchMovesSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]

    def parse(self, response):
        types = [
            t.css("a::text").get().lower()
            for t in response.css("div.grid-row > div.grid-col")[1]
            .css("div.resp-scroll")[1]
            .css("table > tbody > tr > th")
        ]

        type_chart = {}
        idx = 0
        for type in (
            response.css("div.grid-row > div.grid-col")[1]
            .css("div.resp-scroll")[1]
            .css("table > tbody > tr")
        ):
            effectiveness = {}
            def_idx = 0
            for data in type.css("td"):
                effectiveness[types[def_idx]] = convert_damage(data.css("::text").get())
                def_idx += 1
            type_chart[types[idx]] = effectiveness
            idx += 1
        return type_chart
