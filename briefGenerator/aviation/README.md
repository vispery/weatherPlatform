### 用法
首先需要Python3环境，执行`pip install -r requirements.txt`安装依赖

安装Selenium ChromeDriver，对于Debian、Ubuntu等系统，执行`sudo apt-get install -y chromium-chromedriver`进行安装

服务器可能还需要安装中文字体以防止乱码：`sudo apt install -y fonts-wqy-zenhei`

在本文件夹用python运行main.py，将会在本文件夹生成brief.docx文档

### 爬取数据的格式
每条记录包含name字段为运行日期，image字段为航空气象图（未经处理的原始截图），document为一个数组，其中的元素包含name字段为机场名，text数组为原始预报报文，一行为一个元素
