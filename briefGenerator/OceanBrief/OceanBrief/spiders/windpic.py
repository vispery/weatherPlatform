# -*- coding: utf-8 -*-
import scrapy
from OceanBrief.items import WindPicItem


class WindpicSpider(scrapy.Spider):
    name = 'windpic'
    #allowed_domains = ['http://www.nmc.cn/publish/marine/forecast.htm']
    start_urls = ['http://www.nmc.cn/publish/marine/forecast.htm']

    def parse(self, response):
        windpicItem = WindPicItem()
        #风力图的图片
        picUrl = response.xpath('//img/@src').extract()[2]

        windpicItem["windpic"] = picUrl

        yield windpicItem
