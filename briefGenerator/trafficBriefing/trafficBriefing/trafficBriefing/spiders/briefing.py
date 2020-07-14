# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request
from scrapy.selector import Selector

from trafficBriefing.items import TrafficbriefingItem


class BriefingSpider(scrapy.Spider):
    name = 'briefing'
    allowed_domains = ['www.nmc.cn']
    start_urls = ['http://www.nmc.cn/publish/traffic.html']

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        urls = sel.xpath("//*[@id=\"text\"]/div[3]/div/img/@src").extract()
        strs = sel.xpath(
            "/html/body/div[@class='container']/div[@class='row']/div[@class='col-xs-10']/div[@class='bgwhite'][2]/div[@id='text']/div[@class='writing']/p//text()").extract()
        # 样例，可用来进行测试
        # strs = ["中国气象局与交通运输部2020年4月27日联合发布全国主要公路气象预报",
        #         "4月27日20时至28日20时，西藏中南部等地的部分地区有小到中雪或雨夹雪。内蒙古东北部、东北地区中南部、云南西部等地的部分地区有小雨，其中，云南西南部局地有中雨。另外，江苏中部、安徽北部、河南东部、江西中部、湖南中部、广东西部、广西东部、海南岛北部等地局地有雾。",
        #         "受小到中雪或雨夹雪影响的主要路段有：", "109国道西藏安多—那曲段、西藏当雄境内路段、拉萨境内路段", "219国道新疆赛图拉—大红柳滩—西藏那木如段", "317国道西藏索县—指隆—廓玛段",
        #         "318国道西藏墨竹工卡—达资段、西藏仁布—日喀则—聂拉木段", "受沙尘暴影响的主要路段有：", "100009国道西藏安多—那曲段、西藏当雄境内路段、拉萨境内路段",
        #         "219国道新疆赛图拉—大红柳滩—西藏那木如段", "317国道西藏索县—指隆—廓玛段", "318国道西藏墨竹工卡—达资段、西藏仁布—日喀则—聂拉木段", "受雾影响的主要路段有：",
        #         "京沪高速(G2)江苏淮安境内路段、江苏高邮—江都段", "京台高速(G3)安徽宿州—蚌埠段", "京港澳高速(G4)湖南衡山境内路段", "沈海高速(G15)江苏盐城—东台段、广东湛江境内路段",
        #         "长深高速(G25)江苏淮安—洪泽段", "淮徐高速(G2513)江苏淮安境内路段", "济广高速(G35)安徽阜阳境内路段", "宁洛高速(G36)南京境内路段、安徽明光—蚌埠—阜阳—界首段",
        #         "沪陕高速(G40)江苏九华—泰兴—扬州段、安徽全椒境内路段", "扬溧高速(G4011)江苏扬州—镇江段", "沪蓉高速(G42)安徽全椒境内路段", "大广高速(G45)河南平舆境内路段",
        #         "沪昆高速(G60)湖南娄底境内路段", "福银高速(G70)江西南城境内路段", "兰海高速(G75)桂粤省界境内路段", "海南环线(G98)海口—海南定安段、海口境内路段",
        #         "宁靖盐高速江苏盐城境内路段", "宁宿徐高速江苏盱眙境内路段", "宿淮高速江苏建湖—盐城段", "新阳高速河南新蔡境内路段", "海文高速海口境内路段、海南文昌境内路段",
        #         "104国道安徽五河—滁州—南京段", "105国道安徽太和—阜阳—扈胡段", "106国道河南新蔡境内路段", "107国道湖南湘潭—衡山段", "204国道江苏盐城—东台—海安段",
        #         "205国道江苏观音寺境内路段", "206国道安徽蚌埠—淮南—合肥段、江西南城—南丰段", "207国道湖南涟源境内路段", "223国道海口—海南三门坡段",
        #         "224国道海口境内路段、海南琼中境内路段", "312国道南京—安徽全椒段", "316国道福建光泽境内路段", "320国道湖南湘乡—双峰段", "324国道广西北流境内路段",
        #         "325国道广东遂溪—粤桂省界段", "328国道南京—江苏扬州—泰州—江苏海安全线"]
        snow_influenced = []
        fog_influenced = []
        rain_influenced = []
        thunder_influenced = []
        other_influenced = []

        pattern = '的主要路段有：'
        # 利用浅拷贝
        temp_influenced = []
        begin = False
        for i, str in enumerate(strs):
            if pattern in str:
                begin = True
                if '雪' in str:
                    temp_influenced = snow_influenced
                    temp_influenced.append(str)
                    continue
                elif '雾' in str:
                    temp_influenced = fog_influenced
                    temp_influenced.append(str)
                    continue
                elif '雨' in str:
                    temp_influenced = rain_influenced
                    temp_influenced.append(str)
                    continue
                elif '雷' in str:
                    temp_influenced = thunder_influenced
                    temp_influenced.append(str)
                    continue
                else:
                    temp_influenced = []
                    temp_influenced.append(str)
                    other_influenced.append(temp_influenced)
                    continue
            else:
                if not begin:
                    continue
                else:
                    for each in str.split('、'):
                     temp_influenced.append(each)
        item = TrafficbriefingItem()
        item['img_urls'] = urls
        item['snow_influenced'] = snow_influenced
        item['fog_influenced'] = fog_influenced
        item['rain_influenced'] = rain_influenced
        item['thunder_influenced'] = thunder_influenced
        item['other_influenced'] = other_influenced

        yield item
