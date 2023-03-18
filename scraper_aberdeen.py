from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
from datetime import datetime as dt
# import mysql.connector

from .db import get_session, Body, Request, Document, RequestTag

def scrape(url, year):
	html = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(html)
	tags1 = [x.lower().strip() for x in soup.title.string.split(" and ")]
	tags = []
	for x in tags1:
		tags.extend(x.split(" - "))
	tags.append('aberdeen')
	tags.append('aberdeen city')
	reqs = [{'doc': x.get('href', None), 'title': x.string.split(' - ')[1], 'iden': x.string.split(' - ')[0], 'type': x.string[0:3], 'date': dt.strptime(year, '%Y'), 'tags': tags} for x in soup.table.findAll('a')]
	return reqs

def im(reqs, body_id):
	session = get_session()
	for req in reqs:
		if len(session.query(Request).filter(
				Request.body_req_id == req['iden']).all()) == 0:
			r = Request(body = body_id,
				    body_req_id = req['iden'],
				    title = req['title'],
				    type = req['type'])
			session.add(r)
			session.commit()
			doc = Document(request=r.id,
				       url = req['doc'])
			session.add(doc)
			session.commit()
			for tag in req['tags']:
				t = RequestTag(request=r.id,
					       tag=tag)
				session.add(t)
				session.commit()
			
urls = ['http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/arts_and_leisure_2014.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/bereavement_2014.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/contracts_and_procurement_2014.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/decisions_policies_plans_2014.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/education_2014.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/environment_2014.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/financial_information_2014.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/housing_2014.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/it_and_communication_2014.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/land_and_property_2014.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/legal_and_licensing_2014.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/parking_2014.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/roads_and_transport_2014.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/social_care_2014.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosurelog2014/staffing_2014.asp']

urls13 = ['http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/arts_and_leisure.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/bereavement.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/contracts_procurement.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/decisions-policies-plans.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/education_dl.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/environment_dl.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/financial_information_dl.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/housing_dl.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/it_communication.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/land_property_dl.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/legal_and_licensing.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/parking_dl.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/roads_and_transport.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/social_care_adults.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/social_care_children.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/social_care_elderly.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/social_care.asp', 'http://www.aberdeencity.gov.uk/council_government/dp_foi/freedom_information/disclosure_log/staffing.asp']

for url in urls:
	im(scrape(url, "2014"), 1) # should really lookup body_id


# for url in urls13:
# 	im(scrape(url, "2013"))

