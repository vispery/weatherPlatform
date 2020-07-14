# -*- coding: utf-8 -*-
from pymongo import MongoClient
import time
import json
import os
import sys
from bson.binary import Binary
import base64
from PIL import Image


jsonFile = open("../trafficBriefing/trafficBriefing/brief.json",mode="r",encoding="utf-8")

jsonLoad = json.load(jsonFile)

client = MongoClient('192.144.229.202',27017)
cur = time.strftime('%Y{y}%m{m}%d{d}',time.localtime(time.time())).format(y='年',m='月',d='日')


onepicUrl = "../trafficBriefing/trafficBriefing/img/"+cur+"全国交通气象预报.png"

onePic = ""

if os.path.exists(onepicUrl):
    onePic = base64.b64encode(open(onepicUrl,mode="rb").read())


db = client['python-db']
col = db['Traffic']
aim={'name':'','document':'','image':''}
aim["name"]=cur
aim["document"]=jsonLoad[0]
aim["image"]= onePic


#col.delete_many({})

filepath="../trafficBriefing/trafficBriefing/img"
del_list = os.listdir(filepath)
for f in del_list:
    file_path = os.path.join(filepath, f)
    if os.path.isfile(file_path):
        if f!=cur+".png":
            os.remove(file_path)

col.insert_one(aim)
'''
for item in col.find(): 
    picdata = item["image"]
    with open('1.png', 'wb') as file:
        data = base64.b64decode(picdata)  
        file.write(data)  
'''