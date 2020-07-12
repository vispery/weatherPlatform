# -*- coding: utf-8 -*-
import scrapy
import re
from OceanBrief.items import OceanbriefItem


class WeathertableSpider(scrapy.Spider):
    name = 'weathertable'
    #allowed_domains = ['http://www.nmc.cn/publish/marine/offshore.html']
    start_urls = ['http://www.nmc.cn/publish/marine/offshore.html']

    def parse(self, response):
        oceanbriefItem = OceanbriefItem()
        #text = response.xpath('string(//*[@id="datatable"]/tbody)').extract()

        #用xpath把海洋部分的风向风力的大表爬下来
        text = response.xpath('//*[@id="datatable"]/tbody').extract()
        #用正则表达式去掉所有的html标签，只留下文字部分
        pattern = re.compile(r'<.*?>', re.S)
        text1 = pattern.sub(" ",text[0])

        oceanbriefItem["text"] = text1
        yield oceanbriefItem
