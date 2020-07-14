# -*- coding: utf-8 -*-
from PIL import Image
import time
import os

p=os.path.dirname(__file__)
p = p[:-5]
source = Image.open('{}/util/font.png'.format(p))
aim = Image.open('{}/0'.format(p))
aim.paste(source, (300, 50))
date = time.strftime('%Y{y}%m{m}%d{d}',time.localtime(time.time())).format(y='年',m='月',d='日')


aim.save(('{}/'+date + '.png').format(p))
os.remove('{}/0'.format(p))