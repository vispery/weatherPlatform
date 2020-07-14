from django.http import HttpResponse
from django.shortcuts import render
import os
from .settings import con

context = {}

ocean = con['python-db'].Ocean
tra = con['python-db'].Traffic
air = con['python-db'].airports
def hello(request):
    return HttpResponse("hello world !")

def homepage(request):


    context["message"] = "test"
    gen = request.GET.get('generator')
    sh = request.GET.get("show")

    if(gen == "gen"):
        print(gen)
        # 切进爬虫目录
        os.chdir("./briefGenerator")

        # 执行爬虫
        os.system("python generator.py")

        # 切回django目录
        os.chdir(os.pardir)
        return render(request,'chongDX.html')
    else:
        pass

    #if sh == "ocean":
       # for o in ocean.find():
         #   context["o_message"] = o["document"]

    #elif sh == "traffic":
    #for t in tra.find():
        #context["t_message"] = t["document"]
    #elif sh == "airport":
       # for a in air.find():
         #   context["a_message"] = a["document"]


    return render(request, 'home_page.html', context)


def traffic(request):
    context["message"] = "test"
    for t in tra.find():
        context["t_message"] = t["document"]

    return render(request,'traffic.html',context)

def oceanSure(request):
    context["message"] = "test"
    for o in ocean.find():
        context["o_message"] = o["document"]

    return render(request,'ocean.html',context)

def airport(request):
    context["message"] = "test"
    for a in air.find():
        context["a_message"] = a["document"]

    return render(request,'airport.html',context)

def test(request):
    return  render(request , 'test.html')

def generateSpider(request):
    # 切进爬虫目录
    os.chdir("./briefGenerator")

    # 执行爬虫
    os.system("python generator.py")

    # 切回django目录
    os.chdir(os.pardir)
    return render(request, 'test.html')

def spider(request):
    return  render(request,'spider.html')