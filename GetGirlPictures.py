# -*- coding: utf-8 -*-

from urllib import request
import re
from bs4 import BeautifulSoup
import time
# import threading
# from multiprocessing.dummy import Pool 
from threading import Thread
import os

historyList=[]
directory=""

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

    global historyList 
    global directory
    path="/home/joey/download"+directory
    if  not os.path.exists(path):
        os.mkdir(path)
    try:

        index = len(imgurl)
        if index>0:
            imgUrlReal=imgurl[0]
            if len(imgUrlReal)>1:
                imgUrl = imgUrlReal[1]
                print(imgUrl)
            
            namestr='{}{}'.format(path,html3.replace('.html','.jpg'))
           # fileName+=1
 
            if  len(historyList)>=0:             
                if  imgUrl not in historyList:
                    request.urlretrieve(url=imgUrl,filename= namestr)
                    historyList.append(imgUrl) 
                    print(namestr)

                      
    except IOError as identifier:
        pass
    return nextimg 

def getAllUrlOnePage(html,mainUrl):
    htmlcontent =getHtml(html)
    pattern =re.compile('href="(/\d{2,10}\.html)"')
    imgList = pattern.findall(htmlcontent)
    #print(htmlcontent)
    #imgList=list(set(imgList))
    imglists=delSame(imgList)
    #print(imglists)
    return imglists


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

class downloadImageThread(Thread):
    def __init__(self,url):
        Thread.__init__(self)
        self.url=url

#def getPictureOnePage(mainUrl,url,fileName):
    def getPictureOnePage(self,url):
        try:

            global mainUrl

            weizhi=1
            imgsHistory=[]
            #5、循环单个图集
            next = getPicture(mainUrl,url,url)
           # imgsHistory.append(next[0])  
            current = re.sub("\D","",url)

            while (len(next)>0 and weizhi>0):
                
                if next[0] in imgsHistory:
                    break 
 
                imgsHistory.append(next[0])  
                next = getPicture(mainUrl,url,next[0])                
                if next:
                    weizhi = next[0].find(str(current))  

               # time.sleep(0.02)
        except IOError as e:
            pass
    def run(self):
       self.getPictureOnePage(self.url)



def delSame(ilist):
    olist = []
    for x in ilist:
        if x not in olist:
            olist.append(x)
    return olist


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
            pageIndex=1   
            if len(urllists)>0:
                urllists.clear()
            print(mainurl)
            directory=mainurl
            while (True):
                after ="/page/{}".format(pageIndex)
                imageUrl = mainUrl+mainurl+after  
                #3、找出单页面所有图集         
                tempList = getAllUrlOnePage(imageUrl,'ishsh')
                if len(tempList)==0:
                    break
               #3.2单页面中的下拉刷新
                urllists+=tempList
                pageIndex+=1

            # 去重
            ##urllists = list(set(urllists))
            urllists = delSame(urllists)
            #print(urllists)

            print('数量是{}'.format(len(urllists)))
            print('*'*100)
            threads = []
            rangeNum=1
            rangeLoops=11

            #4、循环单页面所有地址
            for url in urllists:

                #if rangeNum<rangeLoops:
                for i in range(rangeNum,rangeLoops):#创建10个线程
                    index = urllists.index(url)
                    if index<len(urllists):
                      #  t =threading.Thread(target=getPictureOnePage,args=(url,))
                        t=downloadImageThread(url)
                        threads.append(t)
                        t.start()

                        rangeNum+=1
                        #break  
                    if (rangeNum==rangeLoops):
                        rangeNum=1
                        # for t in threads:
                        #     t.start()
                        # for m in range(rangeNum+1,rangeLoops+1):
                        #     threads[m].join()
                        for t in threads:
                            t.join()
                        print("before")
                        threads.clear()
                        print("after")
                    break    

                #getPictureOnePage(mainUrl,url,fileName)
                #getPictureOnePage(url)
                    # pools = Pool(rangeLoops)
                    # pools.map(getPictureOnePage,threads)
                    # pools.close()                   
                    # pools.join()
                    
        print("完成后退出")

    except IOError as e:
        pass

        
    