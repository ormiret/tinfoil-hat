from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
from datetime import datetime as dt
import json

from foi import FOI

def scrape():
    page = 1  # Site uses 1-based pagination
    read_next_page = True

    foilist = []

    while read_next_page:
        read_next_page, new_fois = scrape_page(page)
        foilist += new_fois
        page += 1

    return foilist


def scrape_page(page_n):
    print('Page ' + str(page_n))
    html = urllib.request.urlopen('https://www.cne-siar.gov.uk/your-council/freedom-of-information/published-fois/?page=' + str(page_n)).read()
    soup = BeautifulSoup(html, 'lxml')

    foilist = []

    for item in soup.article.find_all('div', class_='cnes_listitem'):
        url = urllib.parse.urljoin('https://www.cne-siar.gov.uk/', item.header.find('a').get('href'))
        foilist.append(scrape_request(url))

    return soup_has_next_page(soup), foilist


def soup_has_next_page(soup):
    for a in soup.article.find_all('a', class_='cnes_pagination_link'):
        if a.get('title').lower().find("next") > 0:
            return True
    return False


def scrape_request(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')

    title = soup.article.find('h1', class_='cnes_pagetitle').string.strip()
    print(title)

    tags = ['na h-eileanan siar', 'western isles']

    for strong in soup.article.find_all('strong'):
        if strong.string is not None:
            if strong.string.lower() == 'reference':
                body_id = strong.parent.find_next_sibling().string.strip()
            elif strong.string.lower() == 'category':
                tags.append(strong.parent.find_next_sibling().a.string.lower().strip())
            elif strong.string.lower() == 'request date':
                initial_request_at = convert_to_datetime(strong.parent.find_next_sibling().string.strip())
            elif strong.string.lower() == 'response date':
                last_updated_at = convert_to_datetime(strong.parent.find_next_sibling().string.strip())

    return FOI(title=title, last_updated_at=last_updated_at, initial_request_at=initial_request_at,
               link=url, tags=tags, body_id=body_id)


def convert_to_datetime(string):
    parsed_date = dt.strptime(','.join(string.split(',')[1:]).strip(), '%B %d, %Y')
    return parsed_date if parsed_date.year > 1 else None

if __name__ == "__main__":
    foilist = scrape()

    with open('json_outputs/eilean_siar.json', 'w') as f:
        json.dump([f.serializable() for f in foilist], f, indent=2)
