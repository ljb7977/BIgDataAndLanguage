from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

case_code = "C1"
press = "FOX"
if press == "NYT":
	site = "www.nytimes.com"
elif press == "FOX":
	site = "www.foxnews.com"
elif press == "NYP":
	site = "nypost.com"
elif press == "WSP":
	site = "www.washingtonpost.com"

file = open("_".join([press, case_code, "urls"])+".txt", "w")

keyword = "Nice attack"
starttime = "7/14/2016"
endtime = "8/14/2016"

driver = webdriver.Chrome("C:\chromedriver.exe")
driver.implicitly_wait(3)
driver.get("https://www.google.com")

search = driver.find_element_by_name("q")
search.send_keys(keyword+" site:"+site)
search.send_keys(Keys.RETURN)
input()

button =driver.find_element_by_id("hdtb-tls")
button.click()
time.sleep(0.5)

button = driver.find_element_by_css_selector("#hdtbMenus > div > div:nth-child(5)")
button.click()
time.sleep(0.5)

button = driver.find_element_by_id("cdrlnk")
button.click()
time.sleep(0.5)

date = driver.find_element_by_id("cdr_min")
date.send_keys(starttime)

date = driver.find_element_by_id("cdr_max")
date.send_keys(endtime)

button = driver.find_element_by_css_selector("#cdr_frm > input.ksb.mini.cdr_go")
button.click()
time.sleep(0.5)

'''
while True:
	p = driver.find_elements_by_css_selector("h3 > a")
	for i in p:
		print(i.get_attribute('href'))
		file.write(i.get_attribute('href')+"\n")
	try:
		button = driver.find_element_by_id("pnnext")
	except:
		break
	button.click()

	time.sleep(0.5)
	'''

for i in range(5):
	p = driver.find_elements_by_css_selector("h3 > a")
	for i in p:
		print(i.get_attribute('href'))
		file.write(i.get_attribute('href')+"\n")
	try:
		button = driver.find_element_by_id("pnnext")
	except:
		break
	button.click()

	time.sleep(0.5)