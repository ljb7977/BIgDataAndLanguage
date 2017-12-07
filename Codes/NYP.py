from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import datetime
import bs4

def remove(value):
	for c in '\/:*?"<>|':
		value = value.replace(c,'')
	return value;

def crawl(targetUrl, case_code, press):
	print(targetUrl)
	targetRequest = Request(targetUrl)
	response = urlopen(targetRequest)
	responseText = response.read()

	soup = BeautifulSoup(responseText, "lxml")

	title = soup.select("#article-wrapper > div.box.article.modal-enabled > div.article-header > h1 > a")[0].contents[0]
	title = remove(title)

	p = soup.select("#article-wrapper > div.box.article.modal-enabled > div.article-header > div.entry-content.entry-content-read-more > p")

	date = soup.select("#article-wrapper > div.box.article.modal-enabled > div.article-header > p")[0].contents
	
	date_t = date[0].strip()
	time = date[2].strip()
	date = date_t+" "+time
	
	date_time = datetime.datetime.strptime(date, "%B %d, %Y %I:%M%p")

	date_time = date_time.strftime("%y%m%d_%H%M")

	filename = case_code+"\\"+"_".join([case_code, press, date_time, title])+".txt"
	
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

#targetUrl = "https://nypost.com/2015/01/07/nypd-on-alert-following-paris-terrorist-attack/"
case_code = "A1"
press = "NYP"
links = open(press+"_"+case_code+"_urls.txt")
while True:
	targetUrl = links.readline()
	if not targetUrl:
		break
	crawl(targetUrl, case_code, press)