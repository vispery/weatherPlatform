# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import datetime
import os

import pymongo
from bson import binary


class AviationPipeline(object):
    def open_spider(self, spider):
        #MONGO_URI = 'mongodb://localhost:27017/'
        #MONGO_URI = 'mongodb://root:123ABCdef@123.57.157.75:30017/'
        self.mclient = pymongo.MongoClient('192.144.229.202',27017)
        self.mdb = self.mclient['python-db']
        self.mcol = self.mdb['airports']
        datestr = datetime.date.today().strftime('%Y%m%d')
        self.document = {'name': datestr, 'document': []}

    def process_item(self, item, spider):
        self.document['document'].append(dict(item))
        return item

    def close_spider(self, spider):
        # assume map image is saved before crawling text
        with open('airportmap.png', 'rb') as f:
            data = f.read()
        self.document['image'] = binary.Binary(data)

        self.mcol.insert_one(self.document)
        self.mclient.close()
        os.remove('airportmap.png')
