from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import datetime, bs4

def crawl(targetUrl, case_code, press):
	print(targetUrl)
	targetRequest = Request(targetUrl)
	response = urlopen(targetRequest)
	responseText = response.read()

	soup = BeautifulSoup(responseText, "lxml")

	title = soup.select("#headline")[0].contents[0]

	p = soup.select("#story > div > div.story-body.story-body-1 > p")

	date = soup.select("#story-meta-footer > p > time")[0].attrs['content']
	date = datetime.datetime.strptime(date[:19], "%Y-%m-%dT%H:%M:%S")

	date_time = date.strftime("%y%m%d_%H%M")

	filename = case_code+"\\"+"_".join([case_code, press, date_time, title])+".txt"

	with open(filename, "w", encoding="utf-8") as file:
		file.write(title+"\n\n")
		
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

#targetUrl = "https://www.nytimes.com/2015/01/08/world/europe/charlie-hebdo-paris-shooting.html"
case_code = "A1"
press = "NYT"
links = open(press+"_"+case_code+"_urls.txt", "r")

while True:
	targetUrl = links.readline()
	if not targetUrl:
		break
	crawl(targetUrl, case_code, press)