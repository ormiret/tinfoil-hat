import requests
from bs4 import BeautifulSoup 
import json
from datetime import datetime

from foi import FOI


def scrape(url):
    home = 'http://www.moray.gov.uk'
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    all_ulists = soup.find_all("ul")
    request_list = []
    month_links = []
    for ulist in all_ulists:
        link_list = ulist.find_all("a")
        for link in link_list:
            if link["href"] != "#":
                month_links.append(link["href"])
    # month_links = ["/moray_standard/page_140447.html"]        # For testing smaller sample set
    for month in month_links:
        month_url = home + month
        raw_month = requests.get(month_url).text
        month_soup = BeautifulSoup(raw_month, features="html.parser")
        table = month_soup.table
        rows = table.find_all("tr")
        rows.pop(0)        # Removes table header
        date_tracker = ""
        for row in rows:
            row_data = row.find_all("td")
            temp_date = row_data[0].contents[0]
            tags = ["moray"]
            if temp_date != " ":        # Carries date down table until new date
                date_tracker = temp_date

            date = None

            if date_tracker.strip():
                try:
                    date = datetime.strptime(date_tracker, "%d-%m-%y")
                except ValueError:
                    try:
                        date = datetime.strptime(date_tracker, "%d-%m-%Y")
                    except ValueError:
                        try:
                            date = datetime.strptime(date_tracker, "%d.%m.%y")
                        except ValueError:
                            try:
                                date = datetime.strptime(date_tracker, "%d.%m.%Y")
                            except ValueError:
                                try:
                                    date = datetime.strptime(date_tracker, "%d/%m/%y")
                                except ValueError:
                                    date = datetime.strptime(date_tracker, "%d/%m/%Y")

            if len(row_data) > 2:  # IJB table has no department column
                department = row_data[2].contents[0]
                tags.append(department.lower())
            else:
                department = "Integrated Joint Board"
            name, number, request_url = process_link(row_data, home)

            request_list.append(FOI(last_updated_at=date, title=name, tags=tags,
                           link=request_url, body_id=number))
            # print(request_list[-1])

    return request_list


def process_link(row_data, home):
    link_data = row_data[1].a
    if link_data:  # At least once instance of no link provided
        rel_url = link_data["href"]
        name = link_data.contents[0]
        request_url = home + rel_url

        raw_request = requests.get(request_url).text
        request_soup = BeautifulSoup(raw_request, features="html.parser")
        try:  # At least one instance of <strong> inside h2
            number = request_soup.h2.contents[0][8:]
        except:
            number = "#"
    else:
        name = row_data[1].contents[0]
        number = "#"
        request_url = "#"

    return name, number, request_url


url = 'http://www.moray.gov.uk/moray_standard/page_62338.html'
request_index = scrape(url)

dict_list = []
for f in request_index:
        # print(f)
        dict_list.append(f.serializable())

with open('json_outputs/moray_foi.json', 'w') as file:
    json.dump(dict_list, file, indent=2)
