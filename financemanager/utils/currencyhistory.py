import urllib
import urllib2
from datetime import *
from BeautifulSoup import BeautifulSoup
import re
from decimal import *
import pandas as ps

def fetch_ukforex_historical_exchange_rates(startdate,enddate,curr1,curr2):
	

	sStartDate=startdate.strftime('%Y-%m-%d')
	sEndDate=enddate.strftime('%Y-%m-%d')
	
	print 'Getting exchange rates....%s%s' % (curr1,curr2)

	url = 'http://www.chartflow.com/fx/historybasic.asp'
	values = {'dateFrom1' : sStartDate,
	          'dateTo1' : sEndDate,
			  'ccy1' : curr1,
			  'ccy2' : curr2,
			  'rounder': 6,
			  'period' : 'exact'
	          }

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	html = response.read()
	
	
	
	soup = BeautifulSoup(''.join(html))
	dataTable=soup.find(text=re.compile("Results Of")).findPrevious('table')
	
	cols = dataTable.findAll('td')
	
	dates = [datetime.strptime(cols[i].string,'%d/%m/%Y') for i in range(2,len(cols)-2,2)]
	values = [Decimal(cols[i].string) for i in range(3,len(cols)-2,2)]

	
	df=ps.DataFrame({'crossrate':values},index=dates)
	
	print "...fetched"
	
	return df
	


