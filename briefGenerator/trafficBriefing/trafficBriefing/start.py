import os
import cmd
import time


cmd1="scrapy crawl briefing -o ./trafficBriefing/brief.json -s FEED_EXPORT_ENCODING=UTF-8"
cmd2="python trafficBriefing/img/util/picMod.py"
cmd3="python ../briefGenerator/trainsition.py"
cmd4="python ../briefGenerator/connect_mongodb.py"
if os.path.exists("./trafficBriefing/brief.json"):
 os.remove("./trafficBriefing/brief.json")
os.system(cmd1)
os.system(cmd2)
os.system(cmd4)