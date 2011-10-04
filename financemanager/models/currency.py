from django.db import models
from financemanager.utils.currencyhistory import *
import sys
from financemanager.models.prices import CurrencyPrice
import numpy as np

class Currency(models.Model):
	code=models.CharField(max_length=6,primary_key=True)
	locale_code=models.CharField(max_length=6)

	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return self.code
		
	class Meta:
		verbose_name_plural = "Currencies" #cleans up name in admin
		app_label = "financemanager"

	def fetch_price_frame(self,startdate,enddate):


		try:

			df = fetch_ukforex_historical_exchange_rates(startdate,enddate,self.code,'USD')
			
		except:
			print "Error: ", sys.exc_info()[0]
			print "Error loading uk forex data for %s %s" % (self,str(startdate))
			return None


		return df
		
	def save_price_frame(self,df):

		if df is None:
			return

		for dt in df.index:

			try:
				p=CurrencyPrice.objects.get(date=dt,currency=self)
			except:
				p=CurrencyPrice()

			xs=df.xs(dt)
			
			p.date=dt
			p.price=xs['crossrate']
			p.currency=self
		
			p.save()
		
	def load_price_frame(self,startdate,enddate,curr='USD'):


		#if currency is other than USD, load it's frame for crossrate calculation
		crosscurr=None
		if curr != 'USD':
			try:
				crosscurr=Currency.objects.get(code=curr)
			
				pdf_cross=crosscurr.load_price_frame(startdate,enddate,'USD')
			except:
				print 'Could not load %s, defaulting to USD' % curr
				crosscurr=None
				curr='USD'
				
		
		#load prices into a numpy array
		if startdate is None:
			qs=CurrencyPrice.objects.filter(date__lte=enddate,currency=self)
		else:
			qs=CurrencyPrice.objects.filter(date__lte=enddate,date__gte=startdate,currency=self)

		vlqs = qs.values_list()
		prices = np.core.records.fromrecords(vlqs, names=[f.name for f in CurrencyPrice._meta.fields])
		dates = [datetime.combine(d,time()) for d in prices.date]
	

		data={
			'crossrate': prices.price,
		}

		pdf=ps.DataFrame(data,index=dates)	
		
		#perform cross currency calcs
		if crosscurr is not None:
			pdf_cross=pdf_cross.reindex(dates)
			
			data={
				'crossrate': pdf['crossrate']/pdf_cross['crossrate']
			}
			
			pdf=ps.DataFrame(data,index=dates)	
		
			

		return pdf