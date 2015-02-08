import urllib, urllib2, re
from bs4 import BeautifulSoup 

def scrape(url):
	home = 'http://www.moray.gov.uk/'
	datePattern = r'[0-9][0-9]-[0-9][0-9]-20[0-9][0-9]'	
	departments = r'(Chief Executive\'s Office|Corporate Services|Education and Social Care|Environmental Services|Multiple Services)'
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	links = soup.findAll('a', href=True)
	for l in links:
		if l.string is not None:
			#print l.string
			if re.search(departments, l.string) is not None:
				page = urllib2.urlopen(home+l['href']).read()
				pSoup = BeautifulSoup(page)
				pLinks = pSoup.findAll('a', href=True)
				for pl in pLinks:
					if pl.string is not None:
						try:
							if re.search(datePattern, pl.string):
								#print pl.string + ' : ' + pl['href']
								foi = urllib2.urlopen(home+pl['href']).read()
								foiSoup = BeautifulSoup(foi)
								bill = foiSoup.find('div', {'class': 'boxj_txt_ara'})
								if bill is not None:
									print bill.p
						except UnicodeEncodeError:
							pass


				
url = 'http://www.moray.gov.uk/moray_standard/page_62338.html'
scrape(url)