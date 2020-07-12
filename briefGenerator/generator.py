import os
import time
from docx import Document

from aviation import aviast
from OceanBrief import generator as Oceangenerator



def getcur():
    sep = '/'
    if os.getcwd().find(sep) == -1:
        sep = '\\'
    return os.getcwd().split(sep)[-1]

oceanptah = "OceanBrief"
aviationpath = "aviation"
trafficpath = "trafficbriefing"
weatherbriefpath = "weatherbriefing"

cur = time.strftime('%Y{y}%m{m}%d{d}', time.localtime(time.time())).format(y='年', m='月', d='日')

#第一部分完成爬取、数据存储
#第二部分完成简报生成
#简报命名 2020年05月12日简报（cur+"简报"）

#第一部分
#气象概况
if getcur() != weatherbriefpath:
    os.chdir(weatherbriefpath)
os.chdir("./weatherbriefingspider")
os.system("python start.py")
os.chdir("../")
os.chdir("../")
print("============weatherbrief ok================")
#do something
#...

#公路
if getcur() != trafficpath:
    os.chdir(trafficpath)
os.chdir("./trafficBriefing")
os.system("python start.py")
os.chdir("../")
os.chdir("../")
print("============traffic ok================")
#do something
#...


#水路
if getcur() != oceanptah:
    os.chdir(oceanptah)
#do something
#...
os.system("python start.py")
os.chdir("../")
print("============ocean ok================")

#航空
if getcur() != aviationpath:
    os.chdir(aviationpath)
#do something
#...
os.system('scrapy crawl airport')
os.chdir("../")
print("============aviation ok================")

#生成简报
#概述
#公路
#水路
#民航
#公路附件
#水路附件
#民航附件
path = "./"+cur+"简报.docx"
if os.path.exists(path):
    #print(1)
    os.remove(path)

document = Document()
document.save(path)

#概述
os.chdir(weatherbriefpath)
os.chdir("./briefGenerator")
os.system("python MainGenerator.py")
os.chdir("../")
os.chdir("../")
print("============概述 ok================")
#公路

os.chdir(trafficpath)
os.chdir("./briefGenerator")
os.system("python MainGenerator.py")
os.chdir("../")
os.chdir("../")
print("============公路 ok================")
#水路
document = Document(path)
Oceangenerator.firstpart(document)
document.save(path)
print("============水路 ok================")
#民航
document = Document(path)
aviast.firstpart(document)
document.save(path)
print("============民航 ok================")
#公路附件
os.chdir(trafficpath)
os.chdir("./briefGenerator")
os.system("python AddictionGenerator.py")
os.chdir("../")
os.chdir("../")
print("============公路附件 ok================")
#水路附件
document = Document(path)
Oceangenerator.secondpart(document)
document.save(path)
print("============水路附件 ok================")
#民航附件
document = Document(path)
aviast.secondpart(document)
document.save(path)
print("============民航附件 ok================")


