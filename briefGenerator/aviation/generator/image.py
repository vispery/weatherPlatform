from PIL import Image, ImageDraw, ImageFont
from datetime import date, datetime, timedelta, timezone
import pymongo
import os


def datestr():
    timenow = datetime.now(timezone(timedelta(hours=8)))
    tomorrow = timenow+timedelta(days=1)
    since = timenow.strftime("%m月%d日%H时")
    end = tomorrow.strftime("%m月%d日%H时")
    if tomorrow.month == timenow.month:
        end = tomorrow.strftime("%d日%H时")
    return since+'-'+end+'(北京时)'


def getmap():
    #MONGO_URI = 'mongodb://localhost:27017/'
    #MONGO_URI = 'mongodb://root:123ABCdef@123.57.157.75:30017/'
    mclient = pymongo.MongoClient('192.144.229.202',27017)
    mdb = mclient['python-db']
    mcol = mdb['airports']
    datestr = date.today().strftime('%Y%m%d')
    #datestr = '20200506'

    imgdata = mcol.find_one({'name': datestr})['image']
    out = open('airportmap.png', 'wb')
    out.write(imgdata)
    out.close()


def processmap():
    amap = Image.open('airportmap.png')
    box = (520, 200, 1280, 762)
    region = amap.crop(box)
    legend = Image.open('aviation/legend.png')
    legendbox = (43, 464, 250, 530)
    region.paste(legend, legendbox)

    # get a drawing context
    d = ImageDraw.Draw(region)

    fontname = 'aviation/simhei.ttf'
    try:
        ImageFont.truetype(fontname)
    except IOError:
        fontname = 'wqy-zenhei.ttc'
        try:
            ImageFont.truetype(fontname)
        except IOError:
            print('Please install Chinese font wqy-zenhei')
    # draw text
    font = ImageFont.truetype(fontname, size=18)
    d.text((515, 12), "全国航空气象预报", font=font, fill='#000000')
    font = ImageFont.truetype(fontname, size=16)
    d.text((475, 36), datestr(), font=font, fill='#000000')

    region.save("airportmapprocessed.png")
    os.remove('airportmap.png')
