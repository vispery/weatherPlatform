import os

import time
weatherSpider = "scrapy crawl weathertable"
windforecastSpider = "scrapy crawl windforecast"
windpicSpider = "scrapy crawl windpic"
wavepicSpider = "python ./OceanBrief/Wavepic/Wavepic.py"

windModify = "python ./Oceanbrief/windmod.py"
generateOceanBrief = "python ./generator.py"

savedata = "python ./connectDB.py"

def getcur():
    sep = '/'
    if os.getcwd().find(sep) == -1:
        sep = '\\'
    return os.getcwd().split(sep)[-1]


oceanptah = "oceanbrief"

if getcur() != oceanptah:
    os.chdir(oceanptah)
os.chdir("../")

#print(os.getcwd())

os.system(weatherSpider)
os.system(windforecastSpider)
os.system(windpicSpider)
os.system(wavepicSpider)

time.sleep(10)

os.system(windModify)
os.system(savedata)
#os.system(generateOceanBrief)

#os.system(clearcache)
