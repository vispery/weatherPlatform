# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TrafficbriefingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    img_urls = scrapy.Field()
    images = scrapy.Field()

    snow_influenced = scrapy.Field()
    fog_influenced = scrapy.Field()
    rain_influenced = scrapy.Field()
    thunder_influenced = scrapy.Field()
    other_influenced = scrapy.Field()
    pass
