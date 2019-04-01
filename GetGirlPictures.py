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

def getPicture(html1,html2):
    html=html1+html2
    # opener=request.build_opener()
    # chaper_url= url
    # #chaper_url='https://www.ishsh.com/wp-content/uploads/2018/04/hk1-1.jpg'
    # #opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
    # opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0')]
    # request.install_opener(opener)
    # respone = request.urlopen(chaper_url)
    # html= respone.read().decode('utf-8') 
    #request.urlretrieve(url=chaper_url,filename='/home/joey/download/1.jpg')
    htmlcontent = getHtml(html)
    currentId= html2.replace('.html','')
    retxt ='<a class.*?href="{}.*?html".*?<img.*?(src=)?.*?</a>'.format(currentId)

    patternC=re.compile(retxt)
    img = patternC.findall(htmlcontent)
    print(htmlcontent)
    print(img)
    # pattern =re.compile('(?<=<img.*?src=")https?.*?(?=")')
    pattern =re.compile('<img.*?(src=)?"(https?.*?.jpg)"')

    imgList = pattern.findall(htmlcontent)
 
    # 判断是否有SRC=
    global fileName 
    global historyList 
    #imgList.remove(imgList[1])
    try:
        for img in imgList:
            # print(img[1])
            # fileName+=1       
            # request.urlretrieve(url=str(img[1]),filename= '/home/joey/download/{}.jpg'.format(fileName))
            # #print(img)

            # patterSub= re.findall('[^\x00-\xff]',img)
            # if  len(patterSub)>0:
            #     continue
            #index = img.find('src')
            
            #if index>0:
            #imgUrl = img.split('src=')[1]
            if len(img)>1:
                imgUrl = img[1]
                fileName+=1
                if  len(historyList)>0:
                    if  imgUrl not in historyList:
                        request.urlretrieve(url=imgUrl,filename= '/home/joey/download/{}.jpg'.format(fileName))
                        historyList.append(imgUrl)
                        print(imgUrl)
                        print('*'*50)
                        print(historyList)
                else:
                    request.urlretrieve(url=imgUrl,filename= '/home/joey/download/{}.jpg'.format(fileName))
                    historyList.append(imgUrl)
                    print(imgUrl)
                    print('*'*50)
                    print(historyList)        
            # else:    
            #     fileName+=1
            #     if  len(historyList)>0:
            #         if  img not in historyList:
            #             request.urlretrieve(url=img,filename= '/home/joey/download/{}.jpg'.format(fileName))
            #             print(img)
            #             print('*'*50)
            #             print(historyList)
                        
    except IOError as identifier:
        pass

def getAllUrlOnePage(html,mainUrl):
    htmlcontent =getHtml(html)
    pattern =re.compile('href="(/\d{2,10}\.html)"')
    imgList = pattern.findall(htmlcontent)
    print(htmlcontent)
    return imgList

# def getAllUrlOnePage(html,mainUrl):
#     htmlcontent =getHtml(html)
#     pattern =re.compile('href="(https?.*ishsh.com.*\.html)')
#     imgList = pattern.findall(htmlcontent)
#     print(htmlcontent)
#     return imgList

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
            getPicture(mainUrl,url)
    