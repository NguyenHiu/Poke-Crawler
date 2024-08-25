# response.xpath('//h2[@id="evo-g1"]/following-sibling::h2[@id="evo-g2"]/preceding-sibling::div')

import scrapy
import re
import time

def extract_continuous_numbers(text):
    try:
        numbers = re.findall(r"\d+", text)
    except Exception as e:
        print(f"Got {e}, text: {text}")
        raise e
    return int(numbers[0])


class FetchEvolutionByLevelSpider(scrapy.Spider):
    name = "fetch_evolution_by_lv_up"
    allowed_domains = ["pokemondb.net"]

    def __init__(self, start_url="https://pokemondb.net/evolution", *args, **kwargs):
        super(FetchEvolutionByLevelSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        
    def get_id_from_div(self, div):
        return div.css("small::text").get()
        
    def get_evolution(self, from_id, span, next_div, evolution_table):
        if span is None or span.get() is None: return
        if next_div is None or next_div.get() is None:
            # multiple evolution paths
            for path in span.xpath('./*'):
                _child_eles = path.xpath('./*')
                _span_arrow = _child_eles[0]
                _next_div = _child_eles[1]
                self.get_evolution(from_id, _span_arrow, _next_div, evolution_table)
        else:
            to_id = self.get_id_from_div(next_div)
            try: 
                lv = extract_continuous_numbers(span.css('small::text').get())
                if from_id not in evolution_table:
                    evolution_table[from_id] = {
                        "to": to_id,
                        "lv": lv
                    }
            except: 
                print(f"span::text: {span.css('small::text').get()}")

            try: _span_arrow = next_div.xpath('following-sibling::*[1]')
            except: return
            try: _next_div = next_div.xpath('following-sibling::*[2]')
            except: _next_div = None
            self.get_evolution(to_id, _span_arrow, _next_div, evolution_table)
    
    def parse(self, response):
        evolution_table = {}
        for evo_chain in response.xpath(
            '//h2[@id="evo-g1"]/following-sibling::*[preceding-sibling::h2[@id="evo-g1"] and following-sibling::h2[@id="evo-g2"] and self::div]'
        ):
            child_elements = evo_chain.xpath('div/*')
            from_div = child_elements[0]
            from_id = self.get_id_from_div(from_div)
            span_arrow = child_elements[1]
            try: next_div = child_elements[2]
            except: next_div = None
            print(f"from_id: {from_id}")
            print(f"span_arrow::text: {span_arrow.css('small::text').get()}")
            # print(f"next_div: {next_div}")
            self.get_evolution(from_id, span_arrow, next_div, evolution_table)
            
        return evolution_table