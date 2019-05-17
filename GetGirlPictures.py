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
    html=html1+html3
    htmlcontent = getHtml(html)
    currentId= html2.replace('.html','')
    #retxt ='<a class.*?href="\{}.*?html".*?<img.*?(src=)?.*?a>'.format(currentId)
    #retxt ='<a class.*?href="{}.*?html".*?<img.*?a>'.format(currentId)
    retxt ='<a class.*?href=".*?html".*?<img.*?a>'
    patternC=re.compile(retxt)
    img = patternC.findall(htmlcontent)

    # 下一页地址
    nextretxt ='href="({}.*?html)"'.format(currentId)
    nextpatternC=re.compile(nextretxt)
    nextimg = nextpatternC.findall(str(img))

    # 图片地址
    reimg=r'<img.*?(src=)?"(https?.*?.jpg)"'
    pattern =re.compile(reimg)
    imgurl = pattern.findall(str(img))
    #print(imgurl)


    global historyList 
    global directory
    path="/home/bing/download"+directory
    if  not os.path.exists(path):
        os.makedirs(path)
    try:

        index = len(imgurl)
        if index>0:
            imgUrlReal=imgurl[0]
            if len(imgUrlReal)>1:
                imgUrl = imgUrlReal[1]
                print(imgUrl)
            
            namestr='{}{}'.format(path,html3.replace('.html','.000'))

 
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
    # 旧方法
    # pattern =re.compile('href="(/\d{1,10}\.html)"')
    # imgList = pattern.findall(htmlcontent)
    #imgList=list(set(imgList))
    #imglists=delSame(imgList)

    urlsoup = BeautifulSoup(htmlcontent, 'html.parser')  
    img_url = urlsoup.find_all('a',attrs={'class':'img'})
    img_url = re.findall('href="(/\d{1,10}\.html)"',str(img_url))

    countsoup = BeautifulSoup(htmlcontent, 'html.parser')  
    imgCount = countsoup.find_all('div',attrs={'class':'btns-sum'})
    img_count = re.findall('(\d{1,10})',str(imgCount))

   # dic= dict(map(lambda x,y:[x,y],img_url,img_count))

    #print(imglists)
   # return imglists
    return img_url,img_count


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
    def __init__(self,url,urlcount):
        Thread.__init__(self)
        self.url = url
        self.urlcount=urlcount

#def getPictureOnePage(mainUrl,url,fileName):
    def getPictureOnePage(self,url,urlcount):
        try:

            global mainUrl

            #5、循环单个图集
            #next = getPicture(mainUrl,url,url)
            # while (len(next)>0):                
            #     next = getPicture(mainUrl,url,next[0])                

            #    # time.sleep(0.02)

            print('地址：{}，图集数量{}'.format(url,urlcount[url]))
            imgcount= int(urlcount[url])
            for i in range(1,imgcount+1):
                imgPage=url.replace('.html','_{}.html'.format(i))
                getPicture(mainUrl,url,imgPage) 
            print('{}图集下载完毕'.format(url))



        except IOError as e:
            pass
    def run(self):
       self.getPictureOnePage(self.url,self.urlcount)



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
    countlists=[]
    #temp
    # temp=[]
    # temp.append(mainUrlLists[len(mainUrlLists)-1])
    # mainUrlLists =temp

    try:
        #2、循环所有主目录
        for mainurl in mainUrlLists:
            pageIndex=1   
            if len(urllists)>0:
                urllists.clear()
            print(mainurl)
            directory=mainurl
            #最后一页时error跳出
            try:
                while (True):
                    after ="/page/{}".format(pageIndex)
                    imageUrl = mainUrl+mainurl+after  
                    #3、找出单页面所有图集         
                    tempList = getAllUrlOnePage(imageUrl,'ishsh')
                    if len(tempList[0])==0:
                        break
                    #3.2单页面中的下拉刷新
                    urllists+=tempList[0]
                    countlists+=tempList[1]
                    pageIndex+=1
            except Exception as identifier:
                pass


            # 去重
            ##urllists = list(set(urllists))
            #此方法不能去重
            #urllists = delSame(urllists)
            #countlists=delSame(countlists)
            #print(urllists)
            imgdic= dict(map(lambda x,y:[x,y],urllists,countlists))

            print('数量是{}'.format(len(urllists)))
            print('*'*100)
            threads = []
           # rangeNum=1
            #线程数
            rangeLoops=20       

            threadUrlList=[]
            # urlItem='/139.html'
            # imgdic={'/139.html':'18'}
            # t=downloadImageThread(urlItem,imgdic)
            # threads.append(t)
            # for t in threads:               
            #     t.start()
            # for t in threads:
            #     t.join(100)
            try:
                #4、循环单页面所有地址   
                while len(urllists)>0:
                    if rangeLoops>len(urllists):
                        rangeLoops= len(urllists)
                    for i in range(rangeLoops):
                        if len(urllists)>i:
                            threadUrlList.append(urllists[i])
                    for urlItem in threadUrlList:
                        t=downloadImageThread(urlItem,imgdic)
                        threads.append(t)

                    for t in threads:     
                        time.sleep(0.3)              
                        t.start()
                    for t in threads:
                        t.join(100)

                    for item in threadUrlList:
                        urllists.remove(item)

                    threads.clear()
                    threadUrlList.clear()
                    rangeLoops=20    

            except Exception as identifier:
                pass
            


            # 线程池
                #getPictureOnePage(mainUrl,url,fileName)
                #getPictureOnePage(url)
                    # pools = Pool(rangeLoops)
                    # pools.map(getPictureOnePage,threads)
                    # pools.close()                   
                    # pools.join()
                    
        print("完成后退出")

    except IOError as e:
        pass

        
    
