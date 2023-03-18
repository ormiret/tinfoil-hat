from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
from datetime import datetime as dt
import json

from foi import FOI


def scrape(year):  # Years between 2018 and 2020 are confirmed to work here
    html = urllib.request.urlopen('https://www.aberdeencity.gov.uk/services/council-and-democracy/access-information/disclosure-log-' + str(year)).read()
    soup = BeautifulSoup(html, "lxml")

    foilist = []
    for a in soup.article.find_all('a'):
        url = urllib.parse.urljoin('https://www.aberdeencity.gov.uk', a.get('href'))
        if url[0:len("https://www.aberdeencity.gov.uk/")] == "https://www.aberdeencity.gov.uk/":
            foilist += scrape_category(url, year)

    return foilist

def scrape_category(url, year):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    tags = soup.title.string.split(':')[1].split('|')[0].strip().lower().split(' and ')
    tags.append('aberdeen')
    tags.append('aberdeen city')
    foilist = []

    for x in soup.article.find_all('a'):
        title = ' '.join(x.string.split(' ')[1:]).strip("- ")
        last_updated_at = dt.strptime(str(year), '%Y')
        link = x.get('href', None)
        body_id = x.string.split(' ')[0]

        foilist.append(FOI(title=title, last_updated_at=last_updated_at,
                     link=link, tags=tags, body_id=body_id))
    return foilist


if __name__ == "__main__":
    foilist = []
    for year in range(2016, 2021):
        yfoilist = scrape(year)
        print(f'First of {year}:')
        print(yfoilist[0])
        print()
        print(f'Last of {year}:')
        print(yfoilist[-1])
        print()
        foilist += yfoilist
    with open('json_outputs/aberdeen.json', 'w') as f:
            json.dump([f.asdict() for f in foilist], f, indent=2)
