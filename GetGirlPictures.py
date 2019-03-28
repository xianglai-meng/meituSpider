# -*- coding: utf-8 -*-

from urllib import request
import re

fileName = 0
historyList=[]

def getPicture(url):
    opener=request.build_opener()
    chaper_url= url
    #chaper_url='https://www.ishsh.com/wp-content/uploads/2018/04/hk1-1.jpg'
    #opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
    opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0')]
    request.install_opener(opener)
    respone = request.urlopen(chaper_url)
    html= respone.read().decode('utf-8') 
    #request.urlretrieve(url=chaper_url,filename='/home/joey/download/1.jpg')

    pattern =re.compile('(?<=<img src=")https?.*?(?=")')

    imgList = pattern.findall(html)
    # 判断是否有SRC=
    global fileName 
    global historyList 
    #imgList.remove(imgList[1])
    try:
        for img in imgList:
        # fileName+=1       
            #request.urlretrieve(url=str(img),filename= '/home/joey/download/{}.jpg'.format(fileName))
            #print(img)

            patterSub= re.findall('[^\x00-\xff]',img)
            if  len(patterSub)>0:
                continue
            index = img.find('src')
            if index>0:
                imgUrl = img.split('src=')[1]
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
            else:    
                fileName+=1
                if  len(historyList)>0:
                    if  img not in historyList:
                        request.urlretrieve(url=img,filename= '/home/joey/download/{}.jpg'.format(fileName))
                        print(img)
                        print('*'*50)
                        print(historyList)
                        
    except IOError as identifier:
        pass


def getAllUrl(html,mainUrl):
	opener=request.build_opener()
	chaper_url=html
	opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0')]
	request.install_opener(opener)
	#1\返回对象
	respone = request.urlopen(chaper_url)
	html= respone.read().decode('utf-8') 
	#html= respone.read()

	#2、返回html内容
	#html = requests.get(html).content.decode("utf-8")

	#print(html)

	pattern =re.compile('href="(https?.*?[1-9][0-9]{2,15}\.html)')

	imgList = pattern.findall(html)

	print(imgList)

	return imgList

if __name__ == '__main__':
    urllists = []
    urllists = getAllUrl('https://www.ishsh.com/','ishsh')
    for url in urllists:
        getPicture(url)
    