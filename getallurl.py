# -*- coding: utf-8 -*-

from urllib import request
import requests
import re


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
	#return imgList


if __name__ == '__main__':
	#getAllUrl('https://www.ishsh.com/','ishsh')
	for x in range(1,10):
		print(x)
	str1="1234"
	str2="a"
	s=str1.find(str2)
	print(s)