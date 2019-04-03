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
    #print(img)

    nextretxt ='href="({}.*?html)"'.format(currentId)
    nextpatternC=re.compile(nextretxt)
    nextimg = nextpatternC.findall(str(img))
    #print(nextimg)
    #print(htmlcontent)

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
            namestr='/home/bing/download/{}_{}.jpg'.format(currentId.replace('/',''),fileName)
 
            if  len(historyList)>0:             
                if  namestr not in historyList:
                    request.urlretrieve(url=imgUrl,filename= namestr)
                    historyList.append(imgUrl) 
                    print(namestr)
            else:           
                historyList.append(namestr)
                request.urlretrieve(url=imgUrl,filename= namestr)
                print(namestr)
   

                       
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
    #1、找出网站目录
    mainUrlLists= getAllMainUrl(htmltxt)

    pageIndex=1    
    urllists = []

    try:
        #2、循环所有主目录
        for mainurl in mainUrlLists:
            
            while (True):
                after ="/page/{}".format(pageIndex)
                imageUrl = mainUrl+mainurl+after  
                #3、找出单页面所有图集         
                tempList = getAllUrlOnePage(imageUrl,'ishsh')
                if len(tempList)==0:
                    break;
               #3.2单页面中的下拉刷新
                urllists+=tempList
                pageIndex+=1

            # 去重
            #print(urllists)
            urllists = list(set(urllists))
            #print(urllists)
            #reIndex=0
            #4、循环单页面所有地址
            for url in urllists:

                # reIndex+=1
                # if reIndex>1:
                fileName=0
                try:
                    #5、循环单个图集
                    next = getPicture(mainUrl,url,url)
                    current = re.sub("\D","",url)
                    weizhi=0
                    while (len(next)>0 and weizhi>=0):
                        next = getPicture(mainUrl,url,next[0])
                        if len(next)==0:
                            break
                        weizhi = next[0].find(str(current))
                except IOError as e:
                    pass
    except IOError as e:
        pass
    # next = getPicture(mainUrl,'/25726.html','/25726_17.html')
    # current = re.sub("\D","",'/25726_17.html')
    # weizhi=0
    # while len(next)>0&weizhi>=0:
    #     next = getPicture(mainUrl,'/25726.html',next[0])
    #     weizhi = next[0].find(str(current))
        
    