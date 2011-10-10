from django.db import models
from openportfolioapp.models import Investment,InvestmentManager
import pandas as ps
from openportfolioapp.models.interestrate import InterestRate
from datetime import *
from pandas.core.datetools import bday,DateOffset
from decimal import *
from openportfolioapp.models.prices import SavingsAccountPrice
import numpy as np

class SavingsAccount(Investment):
	""" A savings account Investment object
	"""
	
	class Meta:
		verbose_name_plural = "Savings Accounts" #cleans up name in admin
		app_label = "openportfolioapp"
			
	investment_type='SavingsAccount'
	objects=InvestmentManager()
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return self.investment_type + ":" + self.name		

	def fetch_price_frame(self,startdate,enddate):
				
		dts=ps.DateRange(start=startdate,end=enddate,offset=bday)
		
		i=0
		dividends=[]
		prices=[]
		
		for dt in dts:
			
			irs=InterestRate.objects.filter(date__lte=dt,investment=self).order_by('-date')
			
			if len(irs) == 0:
					return None
			else:
				ir=irs[0]
			
			prices.append(Decimal(1.0))
			dividends.append(ir.annualrate/365)
			
		data={
			'price':prices,
			'dividend':dividends,
		
		}
		df=ps.DataFrame(data,index=dts)
		
		return df
				
		
		
	def load_price_frame(self,startdate,enddate,crosscurr='USD'):


		
		if startdate==enddate:
			startdate=startdate-timedelta(days=5)
		
		if startdate==None:
			qs=SavingsAccountPrice.objects.filter(date__lte=enddate,investment=self).order_by('date')[:1]
		else:
			qs=SavingsAccountPrice.objects.filter(date__lte=enddate,date__gte=startdate,investment=self).order_by('date')[:1]

		if len(qs)==0:
			print "No prices found"
			return None

		vlqs = qs.values_list()
		prices = np.core.records.fromrecords(vlqs, names=[f.name for f in SavingsAccountPrice._meta.fields])

		
		dates = [datetime.combine(d,time()) for d in prices.date]
		crossrates=self.currency.load_price_frame(startdate,enddate,crosscurr)

		crossrates=crossrates.reindex(dates)


		data={
			'close': prices.price,
			'dividend': prices.dividend,
			'crossrate': crossrates['crossrate'],
			'price': prices.price,
		}
		
		
		
		
		pdf=ps.DataFrame(data,index=dates)	
		pdf['price_fc']=pdf['price'].applymap(Decimal)*pdf['crossrate'].applymap(Decimal)
	
	

		return pdf	
		
		
		
	def save_price_frame(self,df):
		
		if df is None:
			return
			

		
		for dt in df.index:
			
			try:
				p=SavingsAccountPrice.objects.get(date=dt,investment=self)
			except:
				p=SavingsAccountPrice()
				
			xs=df.xs(dt)
			
			p.date=dt
			p.investment=self
			
			p.dividend=xs['dividend']
			p.price=xs['price']
			
			p.save()
	
	def fetch_prices(self,startdate,enddate):
		
		return 1
		
	def price_as_at(self,date):
		
		p=SavingsAccountPrice.objects.filter(date__lte=date,investment=self).order_by('-date')

		if len(p)==0:
			return None

		p=p[0]
		return p.price,p.date
		
	def dividend_as_at(self,date):

		p=SavingsAccountPrice.objects.filter(date__lte=date,investment=self).order_by('-date')

		if len(p)==0:
			return None

		p=p[0]
		return p.dividend,p.date
		
	def process_trade(self,trade):

	
			
			
		return