import urllib.request, urllib.error, urllib.parse, re, urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime

from foi import FOI

def scrape():
	html = urllib.request.urlopen("http://www.eastlothian.gov.uk/site/custom_scripts/foi_download_index.php?currentPage=1&itemsPerPage=2000000").read()

	datePattern = r'(January|February|March|April|May|June|July|August|September|October|November|December) 20[0-9][0-9]$'
	idPattern = r'^http://www.eastlothian.gov.uk/download/downloads/id/(?[0-9]+)/.*$'
	soup = BeautifulSoup(html, 'lxml')

	rows = soup.main.find_all('li', class_='list__item')
	foilist = []

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

			tags = ['east lothian']

			timestamp = datetime.strptime(date, "%B %Y")

			foilist.append(FOI(title=title, last_updated_at=timestamp,
					  link=href, tags=tags, body_id=iden))
	return foilist
				

foilist = scrape()
print('Got ', len(foilist), ' results.')
print('First: ', foilist[0])
print('last one:', foilist[-1])
