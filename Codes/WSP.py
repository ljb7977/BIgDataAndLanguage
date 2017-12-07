from bs4 import BeautifulSoup
import bs4
from urllib.request import Request, urlopen
import time as t

def remove(value):
	for c in '\/:*?"<>|':
		value = value.replace(c,'')
	return value;

def crawl(targetUrl):
	print(targetUrl)
	targetRequest = Request(targetUrl)
	try:
		response = urlopen(targetRequest)
	except:
		print("error")
		return
	responseText = response.read()

	soup = BeautifulSoup(responseText, "lxml")
	title = soup.select("#topper-headline-wrapper > h1")
	if len(title) == 0:
		title = soup.select("#article-topper > h1")
	title = title[0].contents[0]
	title = remove(title)

	p = soup.select("#article-body > article > p")

	date = soup.select("span.pb-timestamp")
	date = date[0].attrs['content'].split('T')
	time = date[1].split('-')[0].split(":")
	time = time[0]+time[1]
	date = date[0].split("-")
	date = str(int(date[0])%100) + date[1] + date[2]

	filename = case+"\\"+case+"_WSP_"+date+"_"+time+"_"+title+".txt"

	with open(filename, "w", encoding="utf-8") as file:
		file.write(title+"\n")
		for i in p:
			para = ""
			for c in i:
				try:
					c = c.contents[0]
				except:
					pass
				if type(c) == bs4.element.Tag:
					continue
				para += c
			file.write(para+"\n")

case = "A1"
links = open("WSP_"+case+"_urls.txt", "r")
while True:
	targetUrl = links.readline()
	if not targetUrl:
		break
	crawl(targetUrl)

	

'''
targetUrl = "https://www.washingtonpost.com/blogs/post-partisan/wp/2015/01/16/stop-being-angry-at-western-media-for-ignoring-boko-haram/?utm_term=.757aa1b9e242"
crawl(targetUrl)
'''
