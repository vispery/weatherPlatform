from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy
from PIL import Image,ImageDraw,ImageFont
import time
import os
cur = time.strftime('%Y{y}%m{m}%d{d}',time.localtime(time.time())).format(y='年',m='月',d='日')
cur0 = time.strftime('%m{m}%d{d}',time.localtime(time.time())).format(m='月',d='日')
driver = webdriver.Chrome()
driver.get("http://www.oceanguide.org.cn/hyyj/seasDetail/offshore-meshing.htm")

driver.maximize_window()

time.sleep(5)

try:
	map = driver.find_element_by_id('map')
	driver.execute_script("arguments[0].scrollIntoView();", map)
	path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

	map.screenshot(path+"/img/"+cur+"map.png")

except BaseException as msg:
	print(msg)

driver.quit()

file1 = path+'/img/mapexp.png'
file2 = path+"/img/"+cur+"map.png"

image = Image.open(file2)  # 原图，缺少标题，带障碍物 640*620
image0 = Image.open(file1)  # 样例图 567*512
image_end = Image.new('RGB',(567, 582), (255, 255, 255))  # 新建空白图片用于制作最后成图
image_pct = Image.new('RGB', (567, 512), (255, 255, 255))  # 新建空图用于制作图片
image_words = Image.new('RGB', (567, 70), (255, 255, 255))  # 新建空图用于制作标题
box0 = (0, 12, 567, 524)  # 大框
box1 = (0, 0, 151, 60)  # 左上角框
box2 = (507, 214, 567, 512)  # 右下角框

image1 = image.crop(box0)
image_pct.paste(image1, (0, 0, 567, 512))
image2 = image0.crop(box1)
image_pct.paste(image2, box1)
image3 = image0.crop(box2)
image_pct.paste(image3, box2)

txt1 = '全海域浪高图'
txt2 = cur0 + '20时（北京时）'
setFond = ImageFont.truetype(path + '/kaiti.TTF', 20)  # 设置字体字号
draw1 = ImageDraw.Draw(image_words)
draw1.text((220, 15), txt1, font=setFond, fill='black')
draw1 = ImageDraw.Draw(image_words)
draw2 = ImageDraw.Draw(image_words)
draw2.text((180, 45), txt2, font=setFond, fill='black')
draw2 = ImageDraw.Draw(image_words)

image_end.paste(image_words, (0, 0, 567, 70))
image_end.paste(image_pct, (0, 70, 567, 582))
image_end.save(file2)
