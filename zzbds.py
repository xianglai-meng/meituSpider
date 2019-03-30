# coding='utf-8'
import re
from bs4 import BeautifulSoup

with open('/home/joey/文档/1.txt') as file_object:
    contents = file_object.read()

soup = BeautifulSoup(contents, 'html.parser')  
catalog = soup.find_all('li',{'id':re.compile("menu-item")})

mainUrlList=[]
for urllist in catalog:
    pattern =re.compile('href="(.*)"')
    urlstr =pattern.findall(str(urllist))
    if len(urlstr[0])<20:
        mainUrlList.append(urlstr[0])
    
print(mainUrlList)




# for link in soup.find_all('a'): #soup.find_all返回的为列表
#     print(link.get('href'))

# catalog = soup.find_all('li',{'id':re.compile("menu-item")})

# pattern =re.compile('(?<=<img src=")https?.*?(?=")')

# imgList = pattern.findall(contents)
# # 判断是否有SRC=
# fileName =0
# #patterSub= re.compile('(?<=src=)https?.*?(?=")')
# for img in imgList:
#     index = img.find('src')
#     if index>0:
#         imgUrl = img.split('src=')[1]
#         fileName+=1
#         imgUrl = imgUrl.encode(encoding='UTF-8',errors='strict')
#         #request.urlretrieve(url=imgUrl,filename= '/home/joey/download/{}.jpg'.format(fileName))
#         print(img)
#     else:    
#         fileName+=1
#         #request.urlretrieve(url=img,filename= '/home/joey/download/{}.jpg'.format(fileName))
#         print(img)


#print(imgList)
#for i in range(0,count):
 #   print(imgList[i])

