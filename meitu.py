# -*- coding: utf-8 -*-

from urllib import request
import re
from bs4 import BeautifulSoup


from threading import Thread
import os

def getHtml(url):
    opener=request.build_opener()
    chaper_url= url

    opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0')]
    request.install_opener(opener)
    respone = request.urlopen(chaper_url)
    html= respone.read().decode('utf-8') 
    return html

def getPicture(html1,html2,html3):
    #html=html1+html2
    html=html1+html3
    htmlcontent = getHtml(html)
    currentId= html2.replace('.html','')
    #retxt ='<a class.*?href="\{}.*?html".*?<img.*?(src=)?.*?a>'.format(currentId)
    retxt ='<a class.*?href="{}.*?html".*?<img.*?a>'.format(currentId)
    patternC=re.compile(retxt)
    img = patternC.findall(htmlcontent)
    #print(img)

    nextretxt ='href="({}.*?html)"'.format(currentId)
    nextpatternC=re.compile(nextretxt)
    nextimg = nextpatternC.findall(str(img))

    return nextimg


if __name__ == "__main__":
	getPicture('https://ishsh.com','/25300.html','/25300_19.html')