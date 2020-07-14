import requests
import scrapy
from ..items import AviationItem


def iscnicao(icao: str):
    if icao[0] == 'Z' and icao[1] != 'K' and icao[1] != 'M':
        return True
    if icao.startswith(("VH", "VM", "RC")):
        return True
    return False


class AirportSpider(scrapy.Spider):
    name = "airport"

    def start_requests(self):
        r = requests.get("http://aviation.nmc.cn/json_data/all.json")
        baseUrl = 'http://aviation.nmc.cn/json_data/html/'
        for ap in r.json()["data"]:
            if iscnicao(ap['icao']):
                # print(ap['airportName'])
                yield scrapy.Request(url=baseUrl + ap['icao'] + ".html", callback=self.parse)

    def parse(self, response):
        try:
            name: str = response.css('.name::text').get()
            pre: str = response.xpath(
                '//*[@id="taf_panel"]/div[2]/pre/text()').get()

            item = AviationItem()
            item['name'] = name
            item['text'] = pre.splitlines()
            yield item

        except Exception:
            # TODO
            pass
