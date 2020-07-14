# -*- coding: utf-8 -*-
import scrapy
import numpy
from PIL import Image,ImageDraw,ImageFont
import time
import os

path = os.path.abspath(os.path.dirname(__file__))
file1 = path+'/img/windexp.png'
file2 = path+'/img/windpic.png'

class windmodify():
    name = 'windmod'
    image = Image.open(file2)   # 原图，带错误标题和龙头 795*793
    image_end = Image.new('RGB',(795,793),(255,255,255)) # 新建空白图片用于制作最后的成图
    image_words = Image.new('RGB', (795, 40), (255, 255, 255))  # 新建空白条图用于编写标题
#   print ('%d %d\n'%(image.size[0], image.size[1]))
#   795 * 793

    box1 = (0,40,795,793)   #   标题以下框
    box2 = (10,10,100,400)    #   左上角龙头框
    image1 = image.crop(box1)    # 裁下原图下半部分（除标题）
    image_end.paste(image1,box1)  # 粘贴图片的下半部分
    txt = '全海域海况图'
    setFond = ImageFont.truetype(path+'/kaiti.TTF',20)    # 设置字体字号
    draw = ImageDraw.Draw(image_words)
    draw.text((335, 15), txt, font = setFond, fill = 'black')
    draw = ImageDraw.Draw(image_words)
    image_end.paste(image_words, (0,0,795,40))   # 粘贴图片的标题

    cur = time.strftime('%Y{y}%m{m}%d{d}', time.localtime(time.time())).format(y='年',m='月',d='日')

    image0 = Image.open(file1)  # 样例图
    image2 = image0.crop(box2)  # 裁下样例图左上角
    image_end.paste(image2,box2)    # 粘贴图片左上角
    image_end.save(path+"/img/"+cur+"wind.png")
    #image_end.save("D:/pycharm projects/weather0407/weather0407/image/windmodify.png")
    #image_end.show()
