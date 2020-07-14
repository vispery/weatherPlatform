#爬虫
CURRENT_DIR=$(cd $(dirname $0); pwd)
cd trafficBriefing/trafficBriefing
#如果之前运行过爬虫那么会存在brief.json，再次运行的话是会把内容追加在后面的，这样就不是准确的json格式了，会出错，所以要先删掉
if [ -f "brief.json" ];then
  rm -f brief.json
fi
scrapy crawl briefing -o brief.json -s FEED_EXPORT_ENCODING=UTF-8

#如果同时装有python2和python3那么这里需要改为python3
python $CURRENT_DIR/trafficBriefing/trafficBriefing/img/util/picMod.py

#生成简报
python $CURRENT_DIR/briefGenerator/trainsition.py