from bs4 import BeautifulSoup
import bs4
from urllib.request import Request, urlopen
import time

from selenium import webdriver


def crawl_link(targetUrl, index):
	global num
	browser.get(targetUrl)
	html = browser.page_source
	soup = BeautifulSoup(html, 'lxml')

	if num == 0:
		num = soup.select("#search-container > div.num-found.ng-pristine.ng-valid > span")[0].contents[0]
	if int(num)//10 < index:
		return False

	p = soup.select("#search-container > div > div > div > h3 > a")
	
	for i in p:
		print(i.attrs['href'])
		file.write(i.attrs['href']+"\n")
	return True

file = open("fox_links.txt", "w", encoding="utf-8")
browser = webdriver.PhantomJS("C:\phantomjs.exe")
i=0
num = 0
while True:
	targetUrl = "http://www.foxnews.com/search-results/search?q="
	keyword = "Brussels bombing"  #change this
	keyword = keyword.replace(" ", "%20")
	temp = "&ss=fn&type=story"
	min_date = "2016-03-22"   #change this
	max_date = "2016-04-22"   #change this
	min_date = "min_date="+min_date
	max_date = "max_date="+max_date
	start = "start="+str(i*10)

	targetUrl += "&".join([keyword, temp, min_date, max_date, start])
	print(targetUrl)

	if crawl_link(targetUrl, i) == False:
		break
	i+=1