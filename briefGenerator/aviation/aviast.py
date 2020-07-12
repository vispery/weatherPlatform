import os
from aviation.generator.brief import firstpart, secondpart


def getcur():
    sep = '/'
    if os.getcwd().find(sep) == -1:
        sep = '\\'
    return os.getcwd().split(sep)[-1]


def crawl():
    subpath = 'aviation'
    if getcur() != subpath:
        os.chdir(subpath)
    # do something
    os.system('scrapy crawl airport')
    # go back
    os.chdir('..')
