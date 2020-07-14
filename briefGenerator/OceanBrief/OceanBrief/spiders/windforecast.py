# -*- coding: utf-8 -*-
import scrapy
from OceanBrief.items import WindForecastItem


class WindforecastSpider(scrapy.Spider):
    name = 'windforecast'
    #allowed_domains = ['http://www.nmc.cn/publish/marine/forecast.htm']
    start_urls = ['http://www.nmc.cn/publish/marine/forecast.htm']


    def parse(self, response):
        windforecastitem = WindForecastItem()
        #爬取当日的风力预报
        windtext = response.xpath('//div/p[contains(text(), "未来三天具体预报如下")]/following-sibling::p[1]/text()').extract_first()
        '''
        windtext = response.xpath('//*[@id="text"]/div[3]/p[7]/text()').extract_first()
        if windtext:
            pass
        else:
            windtext = response.xpath('//*[@id="text"]/div[3]/p[6]/text()').extract_first()
        '''
        windforecastitem["windforecast"] = windtext
        #最后的雾情预报，根据“需注意航行安全”定位
        fogtext = response.xpath('//div/p[contains(text(), "航行安全")]/text()').extract_first()

        windforecastitem["fogforecast"] = fogtext

        yield windforecastitem
