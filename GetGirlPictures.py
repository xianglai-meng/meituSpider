# -*- coding: utf-8 -*-

from urllib import request
import re


opener=request.build_opener()
chaper_url='https://www.ishsh.com/'
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
fileName =0
#patterSub= re.compile('(?<=src=)https?.*?(?=")')
imgList.remove(imgList[1])
try:
    for img in imgList:
       # fileName+=1       
        #request.urlretrieve(url=str(img),filename= '/home/joey/download/{}.jpg'.format(fileName))
        #print(img)
        index = img.find('src')
        if index>0:
            imgUrl = img.split('src=')[1]
            fileName+=1
            request.urlretrieve(url=imgUrl,filename= '/home/joey/download/{}.jpg'.format(fileName))
            print(imgUrl)
        else:    
            fileName+=1
            request.urlretrieve(url=img,filename= '/home/joey/download/{}.jpg'.format(fileName))
            print(img)
except IOError as identifier:
    pass


