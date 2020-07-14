### 环境配置
首先要有python3的环境
然后进入项目根目录，运行pip install -r requirements.txt

### 运行

## Linux系统下直接进入项目根目录，运行run.sh脚本即可

## Windows系统下进入/trafficBriefing目录，运行python start.py即可

### 生成物

**简报文件**
项目根目录下的docx文件，其命名为“xxxx年xx月xx日公路”

**数据（即./trafficBriefing/trafficBriefing/brief.json文件）**
[{
	"img_urls": ["http://image.nmc.cn/product/2020/04/28/TRFC/medium/SEVP_NMC_TRFC_SFER_EME_ACHN_L88_P9_20200428120002400_XML_1.jpg?v=1588066251360"],
	"snow_influenced": ["受小雪或雨夹雪影响的主要路段有：", "109国道西藏安多—那曲—当雄段", "拉萨境内路段", "219国道新疆大红柳滩境内路段", "西藏萨嘎—昂仁—拉孜段", "318国道西藏工布江达境内路段", "西藏如多—墨竹工卡—达资段", "拉萨—西藏曲水段", "西藏仁布—日喀则—聂拉木段"],
	"fog_influenced": ["受雾影响的主要路段有：", "京港澳高速(G4)武汉境内路段", "长张高速(G5513)湖南常德境内路段", "沪昆高速(G60)江西樟树境内路段", "105国道江西丰城—樟树段", "107国道武汉境内路段", "207国道湖南临澧—常德段", "319国道湖南太子庙—常德段", "320国道江西高安—上高段"],
	"rain_influenced": ["受大雨影响的主要路段有：", "214国道云南勐满境内路段"],
	"thunder_influenced": [],
	"other_influenced": []
}]

其中img_urls是公路气象图网址

snow_influenced,fog_influenced,rain_influenced,thunder_influenced等表示受xx影响的路段，
可以看见第一个元素为“受小雪或雨夹雪影响的主要路段有：”这样的信息而不是路段，
这是考虑到公报可能标题不是固定的，比如可能过几天换成了“受中到大雪影响的主要路段有：”等，保留该条信息有助于准确生成简报。
我们在爬虫提取snow_influenced时只是考虑是否含有“雪”的字样，公报标题即使与模板里的不完全一样也可以准确提取。
其他几类天气类似。

other_influenced存储的是受除了雪雾雨雷四种天气以外的天气影响的路段信息。是一个二维数组，如：
[["受沙尘暴影响的主要路段有：", "214国道云南勐满境内路段"],["受泥石流影响的主要路段有：", "214国道云南勐满境内路段"]]
设定other_influenced是考虑到公路模板可能没有给全所有天气情况（里面只有雪雾雨雷四种），假如公报中出现了“受沙尘暴影响的主要路段”这样的新天气，我们要保证也提取出来。

**图片**
经处理后的图片存储在./trafficBriefing/trafficBriefing/img文件夹下
其命名为"xxxx年xx月xx日全国交通气象预报.png"
