from pymongo import MongoClient
import time
import json
import os

import base64


path = os.path.abspath(os.path.dirname(__file__))+"/forecast.json"
jsonFile = open(path,mode="r",encoding="utf-8")
jsonLoad = dict(json.load(jsonFile))
#print(path)
client = MongoClient('192.144.229.202',27017)
cur = time.strftime('%Y{y}%m{m}%d{d}',time.localtime(time.time())).format(y='年',m='月',d='日')

windpicUrl =  os.path.abspath(os.path.dirname(__file__))+"/Oceanbrief/img/"+cur+"wind.png"
wavepicUrl = os.path.abspath(os.path.dirname(__file__))+"/Oceanbrief/img/"+cur+"map.png"

windPic = ""
wavePic = ""
if os.path.exists(windpicUrl):
    #print("windpic exists")
    windPic = base64.b64encode(open(windpicUrl,mode="rb").read())
if os.path.exists(wavepicUrl):
    #print("wavepic exists")
    wavePic = base64.b64encode(open(wavepicUrl,mode="rb").read())

db = client['python-db']
col = db['Ocean']

image={'onepic':'','twopic':''}
aim={'name':'','document':'','image':image}
aim["name"] = cur
aim["document"] = jsonLoad
aim["image"]["onepic"] = windPic
aim["image"]["twopic"] = wavePic

#col.delete_many({})

col.insert_one(aim)

'''
for item in col.find():
    print(item["name"])
    print(item["document"])


    windpicdata = item["windpic"]
    with open('1.png', 'wb') as file:
        data = base64.b64decode(windpicdata)  # 解码
        file.write(data)  # 将解码得到的数据写入到图片中
'''