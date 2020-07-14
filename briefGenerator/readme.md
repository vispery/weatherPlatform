### 一、用法
首先需要Python3环境，执行`pip install -r requirements.txt`安装依赖

安装Selenium ChromeDriver，对于Debian、Ubuntu等系统，执行`sudo apt-get install -y chromium-chromedriver`进行安装

服务器可能还需要安装中文字体以防止乱码：`sudo apt install -y fonts-wqy-zenhei`

在本文件夹用python运行generator.py，将会在本文件夹生成“日期+简报.docx”文档

###二、项目说明
aviation用以爬取并生成**航空部分**的简报

oceanbrief用以爬取并生成**水路部分**的简报

trafficbriefing用以爬取并生成**公路部分**的简报

weatherbriefing用以爬取并生成**气象概况**部分的简报

###三、数据库数据格式

数据库中存储的是字典类对象aim，aim的内容样例参考DBexample.png：
```
#img中存的是图片的二进制数据
img={'onepic':'','twopic':'','threepic':''}

#name域是字符串对象
#document、image域是字典类对象
aim={'name':'','document':'','image':img}

```
