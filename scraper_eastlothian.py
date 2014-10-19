
import urllib2, re, urlparse
from bs4 import BeautifulSoup
from datetime import datetime
from scraper_aberdeen import im

def scrape():
	html = urllib2.urlopen("http://www.eastlothian.gov.uk/site/custom_scripts/foi_download_index.php?currentPage=1&itemsPerPage=2000000").read()

	datePattern = r'(January|February|March|April|May|June|July|August|September|November|December) 20[0-9][0-9]$'
	idPattern = r'^http://www.eastlothian.gov.uk/download/downloads/id/(?[0-9]+)/.*$'
	soup = BeautifulSoup(html)

	rows = soup.table.findAll('tr')
	reqs = []

	for x in range(1, len(soup.table.findAll('tr'))):

		cols = rows[x].findAll('td')
		if ( re.search(datePattern, cols[0].string) is not None ):
			title = re.sub(datePattern, '', cols[0].string).strip()
			if title[-1] == '-':
				title = title[:-1].strip()
			date = re.search(datePattern, cols[0].string).group(0)
			iden = urlparse.urlparse(cols[0].a['href']).path.split('/')[4]
			tags = [re.sub(r'^the', '', tag).lower().strip() for tag in cols[3].string.split(" and ")]
			doc = rows[x].findAll('a')[0].get('href', None)

			tags.append('east lothian')

			timestamp = datetime.strptime(date, "%B %Y")
			reqs.append({'title': title,
				     'tags': tags,
				     'date': timestamp,
				     'type': 'FOI',
				     'iden': iden,
				     'doc': doc})
	return reqs
				

reqs = scrape()
print 'Got ', len(reqs), ' results.'
print 'First: ', reqs[0]
print 'last one:', reqs[-1] 
im(reqs, 2)
