import json
import re
import jieba
import pymongo
from datetime import date, datetime, timedelta
from dateutil import parser


def containsKeyword(line: str):
    keys = ['沙', '尘', '雾', '霾', '雪']
    for k in keys:
        if line.find(k) != -1:
            return True
    return False


def dayHour(fulltime: str):
    return fulltime.split('/')[-1].split(':')[0].split(' ')


def badlist():
    #MONGO_URI = 'mongodb://localhost:27017/'
    #MONGO_URI = 'mongodb://root:123ABCdef@123.57.157.75:30017/'
    mclient = pymongo.MongoClient('192.144.229.202',27017)
    mdb = mclient['python-db']
    mcol = mdb['airports']

    badstrlist = []  # 机场恶劣天气列表
    badsetdict = {}  # 每种恶劣天气对应的城市
    badsetdict['有雨'] = set()
    keys = ['雪', '雾', '霾', '沙', '尘']
    for k in keys:
        badsetdict['有'+k] = set()
    badsetdict['风力较强'] = set()

    datestr = date.today().strftime('%Y%m%d')
    for item in mcol.find_one({'name': datestr})['document']:
        city = jieba.lcut(item['name'], cut_all=False)[0]
        if city.find('机场') != -1:
            city = jieba.lcut(item['name'], cut_all=True)[0]

        blockbad = []
        blockbadstrlist = []
        blockcount = 0
        validTime = ''
        for line in item['text']:
            if line.find('有效时间') != -1:
                # previous block's badstr
                if blockbad:
                    blockbadstrlist.append(validTime + '，'.join(blockbad))
                    blockbad = []

                fromTo = line.split('：')[1].split('至')
                if blockcount:
                    fromtime = dayHour(fromTo[0])
                    totime = dayHour(fromTo[1])
                    if fromtime[0] == totime[0]:
                        validTime = fromtime[0]+'日' + \
                            fromtime[1]+'时'+'至'+totime[1]+'时'
                    else:
                        validTime = fromtime[0]+'日' + \
                            fromtime[1]+'时'+'至'+totime[0]+'日' + totime[1]+'时'
                else:
                    starttime = parser.parse(fromTo[0])
                    currenttime = datetime.now()
                    if currenttime-starttime > timedelta(days=1):
                        # data outdated
                        break
                blockcount += 1

            if (containsKeyword(line)
                or (line.find('雨') != -1
                    and line[line.find('雨')-1] != '小'
                    and line[line.find('雨')-1] != '积')):
                blockbad.append(line.split(':')[-1])
                for k in keys:
                    if line.find(k) != -1:
                        badsetdict['有'+k].add(city)
                if line.find('雨') != -1:
                    badsetdict['有雨'].add(city)

            if line.find('能见度') != -1:
                isKm = False
                afterVis = re.findall('能见度(.+?)km', line)
                if afterVis:
                    isKm = True
                else:
                    afterVis = re.findall('能见度(.+?)m', line)
                numstr = re.findall(r"\d+", afterVis[0])[0]
                num = int(numstr)
                if isKm:
                    num *= 1000
                if num <= 2000:
                    blockbad.append('能见度'+str(num)+'m')

            if line.find('风速') != -1:
                wslist = re.findall(r'\d+m/s', line)
                toobig = False
                for s in wslist:
                    if int(s[:-3]) >= 5:
                        toobig = True
                if toobig:
                    blockbad.append(line[line.find('风速'):].replace(':', ''))
                    badsetdict['风力较强'].add(city)

        if blockbad:
            # last block
            blockbadstrlist.append(validTime + '，'.join(blockbad))

        if blockbadstrlist:
            badstrlist.append(item['name'] + '；'.join(blockbadstrlist))

    mclient.close()

    badsetstr = ''
    for badweather in badsetdict:
        if badsetdict[badweather]:
            badsetstr += ('、'.join(badsetdict[badweather])+badweather+'；')

    return {'badstrlist': badstrlist, 'badsetstr': badsetstr[:-1]+'。'}


# print(badlist())
