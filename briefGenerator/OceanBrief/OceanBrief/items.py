# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class OceanbriefItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    pass

class WindForecastItem(scrapy.Item):
    windforecast = scrapy.Field()
    fogforecast = scrapy.Field()
    pass

class WindPicItem(scrapy.Item):
    windpic = scrapy.Field()
    pass
