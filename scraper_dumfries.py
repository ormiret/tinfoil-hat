import urllib, urllib2, re
from bs4 import BeautifulSoup 

def scrape(url, localDir):
	datePattern = r'(January|February|March|April|May|June|July|August|September|November|December) 20[0-9][0-9]'
	home = 'http://www.dumgal.gov.uk/'
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	links = soup.findAll('a', href=True)
	for l in links:
		if l.string is not None:
			if re.search(datePattern, l.string) is not None:
				fname = localDir+l.string+'.doc'
				print fname
				fUrl = home+l['href']
				urllib.urlretrieve(fUrl, fname)
			

url = 'http://www.dumgal.gov.uk/index.aspx?articleid=10032'
localDir = 'C:/pydata/'
scrape(url, localDir)