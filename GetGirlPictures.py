# -*- coding: utf-8 -*-

from urllib import request
import re
from bs4 import BeautifulSoup
import time
# import threading
# from multiprocessing.dummy import Pool 
from threading import Thread
import os
import datetime
from queue import Queue
import pickle



def getHtml(url):
    opener=request.build_opener()
    chaper_url= url
    #chaper_url='https://www.ishsh.com/wp-content/uploads/2018/04/hk1-1.jpg'
    opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0')]
    request.install_opener(opener)
    respone = request.urlopen(chaper_url)
    html= respone.read().decode('utf-8') 
    return html


def getAllUrlOnePage(html,mainUrl):
    htmlcontent =getHtml(html)

    mainsoup = BeautifulSoup(htmlcontent, 'html.parser')  
    main = mainsoup.find_all('div',attrs={'class':'post-thumbnail'})

    urlcountdic={}
    urllist=[]
    try:
        for urlandcount in main:

            img_url = re.findall('href="(/\d{1,10}\.html)"',str(urlandcount))
            img_count = re.findall('<span>(\d{1,10})</span>',str(urlandcount))

            dict1={img_url[0]:img_count[0]}
            urlcountdic.update(dict1)
            urllist.append(img_url[0])
    except Exception as identifier:
        pass
   
    return urllist,urlcountdic


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
    # def __init__(self,mainUrl,url,urlcount,queue):
    def __init__(self,queue):
        Thread.__init__(self)
        # self.url = url
        # self.urlcount=urlcount
        # self.mainUrl=mainUrl
        self.queue=queue

    def getPictureOnePage(self,directory,mainUrl,url,urlcount):
        try:

            imgcount= int(urlcount[url])
            for i in range(1,imgcount+1):
                imgPage=url.replace('.html','_{}.html'.format(i))
                self.getPicture(directory,mainUrl,url,imgPage)
                time.sleep(0.2) 
                #print(imgcount+1)
            print('{}图集下载结束，时间是：{}'.format(url,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))    


        except IOError as e:
            pass

    
    def getPicture(self,directory,html1,html2,html3):
        html=html1+html3
        htmlcontent = getHtml(html)

        retxt ='<a class.*?href=".*?html".*?<img.*?a>'
        patternC=re.compile(retxt)
        img = patternC.findall(htmlcontent)

        # 图片地址
        reimg=r'<img.*?src=?"(https?.*?.jpg)"'
        pattern =re.compile(reimg)
        imgurl = pattern.findall(str(img))
        #print(imgurl)

        path="/home/bing/download"+directory
        if  not os.path.exists(path):
            os.makedirs(path)
        try:
            index = len(imgurl)
            if index>0:
                imgUrl=imgurl[0]
                # imgUrlReal=imgurl[0]
                # if len(imgUrlReal)>1:
                #     imgUrl = imgUrlReal[1]
                print(imgUrl)
                
                namestr='{}{}'.format(path,html3.replace('.html','.jpg'))
           
                    # if  imgUrl not in historyList:
                    #     request.urlretrieve(url=imgUrl,filename= namestr)
                    #     historyList.append(imgUrl) 
                    #     print(namestr)
                if not os.path.exists(namestr):
                    request.urlretrieve(url=imgUrl,filename= namestr)
                    print('下载完成：'+namestr)
                else:
                    print('已存在下载文件：'+namestr)

                        
        except IOError as identifier:
            pass
        #return nextimg 
                
    def run(self):
        if not self.queue.empty():
            task= self.queue.get()
            directory=task[0]
            mainUrl=task[1]
            url=task[2]
            urlcount=task[3]
            self.getPictureOnePage(directory,mainUrl,url,urlcount)



def delSame(ilist):
    olist = []
    for x in ilist:
        if x not in olist:
            olist.append(x)
    return olist

class threadclass(Thread):
    def __init__(self,no):
        Thread.__init__(self)
        self.no=no

    def run(self):
        print(self.no)
        time.sleep(3)
        print('线程结束时间_____:{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

def writetofile(history):
    hisfile = open('/home/bing/download/history.txt','wb')
    pickle.dump(history,hisfile)

def readfile():
    filepath='/home/bing/download/history.txt'
    if not os.path.exists(filepath):
        open(filepath,'wb')

    hisfile = open(filepath,'rb')
    his =[]
    if os.path.getsize(filepath)>0:
        his = pickle.load(hisfile)
    return his

if __name__ == '__main__':
    mainUrl = "https://www.ishsh.com"

    htmltxt = getHtml(mainUrl+"/gaoqing")
    #1、找出网站目录
    mainUrlLists= getAllMainUrl(htmltxt)

    #temp
    # temp=[]
    # for x in range(1,7):
    #     temp.append(mainUrlLists[len(mainUrlLists)-x])
    # mainUrlLists=temp


    q= Queue()
    historyList=[]
    historyList = readfile()

    imgtotal=0
    try:
        #2、循环所有主目录
        for mainurl in mainUrlLists:
            pageIndex=1   
            urllists = []
            countlists={}

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
		           # hisQ.put(tempList[0])
                    countlists.update(tempList[1])
                    pageIndex+=1
            except Exception as identifier:
                pass

            #计算图片总数量
            # for x in urllists:
            #     imgtotal+=int(countlists[x])
            # continue  

            # 去重
            ##urllists = list(set(urllists))
            #此方法不能去重
            #urllists = delSame(urllists)
            #print(urllists)
           # imgdic= dict(map(lambda x,y:[x,y],urllists,countlists))

            print('数量是{}'.format(len(urllists)))
            print('*'*100)

            threads = []
            rangeNum=20
            #线程数
            rangeLoops=rangeNum

            threadUrlList=[]
            deltemp=[]
            #去除历史记录中的数据
            if len(historyList)>0:
                for ul in urllists:
                    if ul in historyList:
                        deltemp.append(ul)
            if len(deltemp)>0:
                for x in deltemp:
                    urllists.remove(x)        
                     
            try:
                #4、循环单页面所有地址   
                while len(urllists)>0:
                    if rangeLoops>len(urllists):
                        rangeLoops= len(urllists)
                    else:
                        rangeLoops=rangeNum
                    print('线程开始时间:{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

                    for i in range(rangeLoops):
                        #threadUrlList.append(urllists[i])
                        #if urllists[i] not in historyList:
                        historyList.append(urllists[i])
                        threadUrlList.append(urllists[i])

                    for urlItem in threadUrlList:
                        q.put([directory,mainUrl,urlItem,countlists])
                        #t=downloadImageThread(mainUrl,urlItem,countlists,hisQ)
                        t=downloadImageThread(q)
                      #  t=threadclass(urlItem)
                        threads.append(t)

                    for t in threads: 
                     #   t.setDaemon(True)                
                        t.start()
      
                    for t in threads:
                        t.join(100)

                    for item in threadUrlList:
                        urllists.remove(item)

                    threads.clear()
                    threadUrlList.clear()
                    writetofile(historyList)
                    print('线程结束时间:{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
  

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
        print(imgtotal)

    except IOError as e:
        pass

        
    
