from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
from datetime import datetime as dt


def scrape(year):  # Years between 2018 and 2020 are confirmed to work here
	html = urllib.request.urlopen('https://www.aberdeencity.gov.uk/services/council-and-democracy/access-information/disclosure-log-' + str(year)).read()
	soup = BeautifulSoup(html, "lxml")

	reqs = []
	for a in soup.article.find_all('a'):
		url = urllib.parse.urljoin('https://www.aberdeencity.gov.uk', a.get('href'))
		if url[0:len("https://www.aberdeencity.gov.uk/")] == "https://www.aberdeencity.gov.uk/":
			reqs += scrape_category(url, year)

	return reqs

def scrape_category(url, year):
	html = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(html, "lxml")
	tags = soup.title.string.split(':')[1].split('|')[0].strip().lower().split(' and ')
	tags.append('aberdeen')
	tags.append('aberdeen city')
	reqs = []

	for x in soup.article.find_all('a'):
		reqs.append({
			'doc': x.get('href', None),
			'title': ' '.join(x.string.split(' ')[1:]).strip("- "),
			'iden': x.string.split(' ')[0],
			'type': x.string[0:3],
			'date': dt.strptime(str(year), '%Y'),
			'tags': tags
		})

	return reqs


if __name__ == "__main__":
	for year in range(2016, 2021):
		reqs = scrape(year)
		print(f'First of {year}:')
		print(reqs[0])
		print()
		print(f'Last of {year}:')
		print(reqs[-1])
		print()
