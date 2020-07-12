# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# -*- coding: utf-8 -*-
import csv
import json
import scrapy
import urllib.request
from OceanBrief.items import OceanbriefItem,WindPicItem,WindForecastItem

from scrapy.pipelines.images import ImagesPipeline
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import re
import os


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class OceanBriefPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(item, OceanbriefItem):
            index = 0

            templist = item["text"].split()

            forecastList = []
            i, j, maxlen = 0, 0, len(templist)
            '''
        这一部分是为了格式化摘取的数据，存入csv文件中

        http://www.nmc.cn/publish/marine/offshore.html
        近海18个海区天气预报 有时是72小时预报，有时是24小时预报
        72小时预报，总数据个数大约是700个
        24小时预报，总数据个数大约是240个
        我们只摘取24小时的预报数据

        下一步是整理0-12小时和12-24小时的数据（风力、浪高取最大区间，天气取0-12小时）
        整理成0-24小时的数据预报(已完成)

        下一步是爬取风力图和浪高图，然后生成简报
            '''
            if maxlen < 600:
                while (i < maxlen):
                    if (j % 7 == 0 and j % 14 != 0):
                        forecastList.append(forecastList[j - 7])
                        j = j + 1
                    else:
                        forecastList.append(templist[i])
                        i = i + 1
                        j = j + 1
            else:
                while (i < maxlen):
                    if (j % 7 == 0 and j % 14 != 0):
                        forecastList.append((forecastList[j - 7]))
                        j = j + 1
                    else:
                        if (i % 37 == 13 and i != 0):
                            i = i + 24
                        if (i >= maxlen):
                            break
                        forecastList.append(templist[i])

                        i = i + 1
                        j = j + 1

            forecastLen = len(forecastList)
            finalForecast = ""
            for i in range(forecastLen):
                if (i % 14 >= 7):
                    continue
                ans = i % 7
                item_0_12 = forecastList[i]
                item_12_24 = forecastList[i + 7]
                if ans == 0:
                    finalForecast = finalForecast + item_0_12 + ','
                elif ans == 1:
                    finalForecast = finalForecast + "00-24" + ","
                elif ans == 2:
                    finalForecast = finalForecast + item_0_12 + ','
                elif ans == 3:
                    finalForecast = finalForecast + item_0_12 + ','
                elif ans == 4:
                    wind_0_12 = item_0_12.split('-')
                    wind_12_24 = item_12_24.split('-')
                    min_0_12 = int(wind_0_12[0])
                    max_0_12 = int(wind_0_12[1])
                    min_12_24 = int(wind_12_24[0])
                    max_12_24 = int(wind_12_24[1])

                    min_0_24 = min_0_12 if min_0_12 < min_12_24 else min_12_24
                    max_0_24 = max_0_12 if max_0_12 > max_12_24 else max_12_24

                    finalForecast = finalForecast + str(min_0_24) + '-' + str(max_0_24) + ','
                elif ans == 5:
                    height_0_12 = float(item_0_12)
                    height_12_24 = float(item_12_24)
                    height_0_24 = height_0_12 if height_0_12 > height_12_24 else height_12_24

                    finalForecast = finalForecast + str(height_0_24) + ","
                elif ans == 6:
                    finalForecast = finalForecast + item_0_12 + '\n'
                pass

            # print(finalForecast)

            with open("./weather.csv", mode="w", encoding="utf-8") as fout:
                if (index == 0):
                    columnName = "海区,时效,天气,风向,风力,浪高,能见度\n"
                    fout.write(columnName)
                    index = 1
                finalList = finalForecast.split('\n')
                for line in finalList:
                    fout.write(line + '\n')

            return item

        elif (isinstance(item, WindForecastItem)):
            windforecast = item["windforecast"]
            fogforecast = item["fogforecast"]
            print("windforecast:"+windforecast)
            print("fogforecast:"+fogforecast)
            dicts = {}
            reader = csv.reader(open("./weather.csv", encoding="utf-8"))

            for line in reader:
                if line:
                    dicts[line[0]] = line[5]
            addition = ""
            if "另外" in windforecast:
                addition = windforecast.split("另外，")[1]
                pattern = re.compile("（.*?）。")
                addition = pattern.sub("",addition)
                if "日" in addition:
                    addition = addition.split("，")[1]+ ";"
            if "雾" in windforecast:
                if "雾" not in windforecast.split("。")[0]:
                    if "雾" not in fogforecast:
                        fogforecast = windforecast.split("。")[1]
                    windforecast = windforecast.split("。")[0]
                else:
                    windforecast = windforecast.split("。")[1]
            ans = ""
            firstcomma = windforecast.split("，", 1)[0]
            if "时至" in firstcomma:
                p = re.compile(r'.*?，')
                windforecast = p.sub('', windforecast, 1)

            windlist = windforecast.split('。')[0].split("，")
            for item in windlist:
                #    print("windlist:"+item)
                if "将有" not in item:
                    continue
                max_wave = 0
                key_area = []
                areaslist = item.split('将有')[0].split('、')
                for areas in areaslist:
                    if "海域" in areas:
                        areas = areas[0:-2]
                    if "和" in areas:
                        areas = areas.split("和")

                        if "部" not in areas[0]:
                            areas[0] = areas[0] + "部"
                        areas[1] = areas[0][0:2] + areas[1][0:2]
                        if "部" not in areas[1]:
                            areas[1] = areas[1] + "部"
                        key_area.append(areas[0])
                        key_area.append(areas[1])
                    else:
                        key_area.append(areas)

                wind = item.split('将有')[1]
                output1 = item.split('将有')[0]

                for item in key_area:
                    if item not in dicts:
                        if "黄海" in item:
                            item = "黄海北部"
                        elif "东海" in item:
                            item = "东海北部"
                        elif "南海" in item:
                            item = "南海西北部"
                        elif "渤海" in item:
                            item = "渤海"
                    if item in dicts:
                        max_wave = max_wave if max_wave > float(dicts[item]) else float(dicts[item])
                if (max_wave != 0):
                    output2 = "风力" + wind[0] + "~" + wind[7] + "级," + "浪高" + str(max_wave) + "米;"
                else:
                    output2 = "风力" + wind[0] + "~" + wind[7] + "级;"
                ans = ans + output1 + output2

            ans = ans + addition
            if "雾" in fogforecast:
                if '；' in fogforecast:
                    if "雾" in fogforecast.split('；')[0]:
                        fogforecast = fogforecast.split('；')[0]
                    else:
                        fogforecast = fogforecast.split('；')[1]
                else:
                    fogforecast = fogforecast.split('。')[0]
                p = re.compile(r'.*?，')
                if "日" in fogforecast:
                    fogforecast = p.sub('', fogforecast, 1)
                if "，其中" in fogforecast:
                    fogforecast = fogforecast.replace("，其中", ";")
                ans = ans + fogforecast
            # print(ans)
            with open("./forecast.txt", mode="w", encoding="utf-8") as fout:
                fout.write(ans)
            with open("./forecast.json", mode="w", encoding="utf-8") as fout:
                lines = json.dumps(dict(forecast=ans), ensure_ascii=False) + "\n"
                fout.write(lines)
            return item

        elif (isinstance(item, WindPicItem)):
            path = os.path.abspath(os.path.dirname(__file__))
            filename = path + "/img/windpic.png"
            if os.path.exists(filename):
                os.remove(filename)
            return item

        return item

    def close_spider(self, spider):
        pass


class WindpicPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if isinstance(item, WindPicItem):
            #print(item["windpic"])
            yield scrapy.Request(url=item["windpic"], meta={'item': item})

    def file_path(self, request, response=None, info=None):
        # cur = time.strftime('%Y年%m月%d日', time.localtime(time.time()))
        # path = cur+"wind.png"
        path = "windpic.png"
        return path

    def item_completed(self, results, item, info):
        return item

