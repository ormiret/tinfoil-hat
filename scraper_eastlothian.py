
import urllib.request, urllib.error, urllib.parse, re, urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime

def scrape():
	html = urllib.request.urlopen("http://www.eastlothian.gov.uk/site/custom_scripts/foi_download_index.php?currentPage=1&itemsPerPage=2000000").read()

	datePattern = r'(January|February|March|April|May|June|July|August|September|November|December) 20[0-9][0-9]$'
	idPattern = r'^http://www.eastlothian.gov.uk/download/downloads/id/(?[0-9]+)/.*$'
	soup = BeautifulSoup(html)

	rows = soup.main.findAll('li', class_='list__item')
	reqs = []

	for row in rows:
		href = row.a.get('href')
		raw_title = row.a.h3.string
		if ( re.search(datePattern, raw_title) is not None ):
			title = re.sub(datePattern, '', raw_title).strip()
			if title[-1] == '-':
				title = title[:-1].strip()
			date = re.search(datePattern, raw_title).group(0)
			iden = urllib.parse.urlparse(href).path.split('/')[4]
			# tags = [re.sub(r'^the', '', tag).lower().strip() for tag in cols[3].string.split(" and ")]

			# tags.append('east lothian')

			timestamp = datetime.strptime(date, "%B %Y")
			reqs.append({'title': title,
				     # 'tags': tags,
				     'date': timestamp,
				     'type': 'FOI',
				     'iden': iden,
				     'doc': href})
	return reqs
				

reqs = scrape()
print('Got ', len(reqs), ' results.')
print('First: ', reqs[0])
print('last one:', reqs[-1])
