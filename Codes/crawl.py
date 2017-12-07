from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import datetime, sys, bs4

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

	if press == "FOX":
		title = soup.select("#content > div > div.main > article > div > h1")[0].contents[0]
		title = remove(title)

		p = soup.select("#content > div > div.main > article > div > div.article-body > div.article-text > p")

		date = soup.select("#content > div > div.main > article > div > div.article-info > div > time")[0].attrs['datetime']
		date = datetime.datetime.strptime(date[:19], "%Y-%m-%dT%H:%M:%S")
		date_time = date.strftime("%y%m%d_%H%M")
	elif press == "NYT":
		title = soup.select("#headline")[0].contents[0]
		title = remove(title)

		p = soup.select("#story > div > div.story-body.story-body-1 > p")

		date = soup.select("#story-meta-footer > p > time")[0].attrs['content']
		date = datetime.datetime.strptime(date[:19], "%Y-%m-%dT%H:%M:%S")
		date_time = date.strftime("%y%m%d_%H%M")
	elif press == "WSP":
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

		date_time = date+"_"+time
	elif press == "NYP":
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
			
#targetUrl = "http://www.foxnews.com/politics/2015/01/07/white-house-condemns-attack-on-french-publication.html"
case_code = sys.argv[1]
press = sys.argv[2]
links = open(press+"_"+case_code+"_urls.txt", "r")
while True:
	targetUrl = links.readline()
	if not targetUrl:
		break
	crawl(targetUrl, case_code, press)

#run this program with command line like (python crawl.py [case_code] [press])