import scrapy


class FetchPokemonsSpider(scrapy.Spider):
    name = "fetch_pokemons"
    allowed_domains = ["pokemondb.net"]
    
    def __init__(self, start_url="https://pokemondb.net/pokedex/game/red-blue-yellow", *args, **kwargs):
        super(FetchPokemonsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url] 
    
    
    def detail_info_parse(self, response, id, name, img, type_1, type_2):
        trs = response.css('div.grid-row:nth-child(2) > div:nth-child(1) > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr')
        stats = {}
        for tr in trs:
            stats[tr.css('th::text').get().lower().replace(' ', '')] = int(tr.css('td::text').get())
        yield {
            "id": id,
            "name": name,
            "img": img,
            "type_1": type_1,
            "type_2": type_2,
            **stats
        }
            
            
    def parse(self, response):
        infocards = response.css('.infocard')
        for infocard in infocards:
            _img = infocard.css('img::attr(src)').get()
            _id = infocard.css('small::text').get()
            _name = infocard.css('.ent-name::text').get()
            _types = infocard.css('.itype::text')
            _type_1 = _types[0].get().lower()
            _type_2 = ''
            if len(_types) >= 2:
                _type_2 = _types[1].get().lower()
            _details_page_url = infocard.css('a::attr(href)').get()
            stats = {}
            if _details_page_url is not None:
                yield response.follow(
                    f"https://pokemondb.net/{_details_page_url}", 
                    callback=self.detail_info_parse,
                    cb_kwargs={
                        "id": _id,
                        "name": _name,
                        "img": _img,
                        "type_1": _type_1,
                        "type_2": _type_2,
                    })
            