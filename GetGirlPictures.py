# -*- coding: utf-8 -*-

from urllib import request
import re
from bs4 import BeautifulSoup

fileName = 0
historyList=[]

def getHtml(url):
    opener=request.build_opener()
    chaper_url= url
    #chaper_url='https://www.ishsh.com/wp-content/uploads/2018/04/hk1-1.jpg'
    #opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
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
    print(img)

    nextretxt ='href="({}.*?html)"'.format(currentId)
    nextpatternC=re.compile(nextretxt)
    nextimg = nextpatternC.findall(str(img))
    print(nextimg)
    #print(htmlcontent)

    # pattern =re.compile('(?<=<img.*?src=")https?.*?(?=")')
    #原有方式:
    # pattern =re.compile('<img.*?(src=)?"(https?.*?.jpg)"')
    # imgList = pattern.findall(htmlcontent)
    reimg=r'<img.*?(src=)?"(https?.*?.jpg)"'
    pattern =re.compile(reimg)
    imgurl = pattern.findall(str(img))
    #print(imgurl)
    # 判断是否有SRC=
    global fileName 
    global historyList 
    #imgList.remove(imgList[1])
    try:

        index = len(imgurl)
        if index>0:
            imgUrlReal=imgurl[0]
            if len(imgUrlReal)>1:
                imgUrl = imgUrlReal[1]
                print(imgUrl)
            fileName+=1
            # if  len(historyList)>0:
            #     if  imgUrl not in historyList:
            #         request.urlretrieve(url=imgUrl,filename= '/home/joey/download/{}_{}.jpg'.format(currentId.replace('/',''),fileName))
            #         historyList.append(imgUrl)
            #         print('*{}*'.format(historyList))   
            # else:
            namestr='/home/joey/download/{}_{}.jpg'.format(currentId.replace('/',''),fileName)
            request.urlretrieve(url=imgUrl,filename= namestr)
            print(namestr)
            #historyList.append(imgUrl)
            #print('*{}*'.format(historyList))       

                       
    except IOError as identifier:
        pass
    return nextimg 

def getAllUrlOnePage(html,mainUrl):
    htmlcontent =getHtml(html)
    pattern =re.compile('href="(/\d{2,10}\.html)"')
    imgList = pattern.findall(htmlcontent)
    #print(htmlcontent)
    return imgList


def getAllMainUrl(html):
    soup = BeautifulSoup(html, 'html.parser')  
    catalog = soup.find_all('li',{'id':re.compile("menu-item")})

    mainUrlList=[]
    for urllist in catalog:
        pattern =re.compile('href="(.*)"')
        urlstr =pattern.findall(str(urllist))
        if len(urlstr[0])<20:
            mainUrlList.append(urlstr[0])

    return mainUrlList


if __name__ == '__main__':
    mainUrl = "https://www.ishsh.com"
    htmltxt = getHtml(mainUrl+"/gaoqing")

    mainUrlLists = getAllMainUrl(htmltxt)

    urllists = []
    for mainurl in mainUrlLists:
        imageUrl = mainUrl+mainurl
        urllists = getAllUrlOnePage(imageUrl,'ishsh')
        for url in urllists:
            #getPicture(mainUrl,url)

            next = getPicture(mainUrl,url,url)
            current = re.sub("\D","",url)
            weizhi=0
            while (len(next)>0 and weizhi>=0):
                next = getPicture(mainUrl,url,next[0])
                if len(next)==0:
                    break
                weizhi = next[0].find(str(current))

    # next = getPicture(mainUrl,'/25726.html','/25726.html')
    # current = re.sub("\D","",'/25726.html')
    # weizhi=0
    # while len(next)>0&weizhi>=0:
    #     next = getPicture(mainUrl,'/25726.html',next[0])
    #     weizhi = next[0].find(str(current))
        
    