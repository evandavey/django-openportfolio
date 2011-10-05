from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from datetime import *
from financemanager.models.price import Price
from financemanager.utils.returns import returns_dmy
from pandas.core.datetools import MonthEnd,YearEnd
from financemanager.utils.returns import returns
from financemanager.utils.returns import geometric_return
from financemanager.models.returns.investmentreturn import InvestmentReturn
import pandas as ps
from decimal import *
import numpy as np

class SubclassingQuerySet(QuerySet):
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model) :
            return result.as_leaf_class()
        else :
            return result
    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()

class InvestmentManager(models.Manager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)

class Investment(models.Model):
	""" A base Investment object
		Investments are issued by Companies
		Investments are held by Portfolios
		Investments are traded by Portfolios
		Investments can be Bank Accounts,Savings Accounts,Listed Equity
		Investments belong to an Asset Class 
	""" 
	
	class Meta:
		verbose_name_plural = "Investments" #cleans up name in admin
		app_label = "financemanager"
	

	name = models.CharField(max_length=255)
	company=models.ForeignKey("Company")
	asset_class=models.ForeignKey("AssetClass")
	currency=models.ForeignKey("Currency")
	content_type = models.ForeignKey(ContentType,editable=False,null=True)
	objects = InvestmentManager()

	def natural_key(self):
	        return (self.name,) + self.content_type.natural_key()
	
	natural_key.dependencies = ['contenttypes.contenttype']

	def save(self, *args, **kwargs):
		if(not self.content_type):
			self.content_type = ContentType.objects.get_for_model(self.__class__)
			super(Investment, self).save(*args, **kwargs)

	def as_leaf_class(self):
		content_type = self.content_type
		model = content_type.model_class()
		if (model == Investment):
			return self
		return model.objects.get(id=self.id)
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return self.name		



	def _latest_price(self):

		price=self.price_as_at(datetime.now())
		
		if price is None:
			return None
		
		return price[0]

	latest_price=property(_latest_price)

	def _latest_price_date(self):

		price=self.price_as_at(datetime.now())

		if price is None:
			return None

		return price[1]

	latest_price_date=property(_latest_price_date)		

	def _latest_dividend(self):

		dividend=self.dividend_as_at(datetime.now())
		
		if dividend is None:
			return None
		
		return dividend[0]

	latest_dividend=property(_latest_dividend)

	def _latest_dividend_date(self):

		dividend=self.dividend_as_at(datetime.now())

		if dividend is None:
			return None

		return dividend[1]

	latest_dividend_date=property(_latest_dividend_date)
	
	
	def mean(self):
		
		enddate=datetime.today()
		
		pdf=self.load_price_frame(None,enddate)
		
		return pdf['price'].applymap(float).mean()
		
	
	def load_returns_frame(self,freq='d'):

		qs=InvestmentReturn.objects.filter(investment=self,freq=freq)


		if len(qs)==0:
			print "No returns found: %s" % self
			return None



		names=['date','P','PP','TR','CR']
		vlqs=[]
		for q in qs:

			tr=q.total_return
			cr=q.capital_return

			if tr is None:
				tr=Decimal('NaN')

			if cr is None:
				cr=Decimal('NaN')

			vlqs.append((q.date,q.price,q.prev_price,tr,cr))

		returns = np.core.records.fromrecords(vlqs, names=names)

		dates = [datetime.combine(d,time()) for d in returns.date]


		data={
			'P': returns.P,
			'PP': returns.PP,
			'TR': returns.TR,
			'CR': returns.CR,

		}

		pdf=ps.DataFrame(data,index=dates)	

		return pdf


	def save_returns_frame(self,df):

		if df is None:
			return

		for dt in df.index:


			xs=df.xs(dt)

			try:
				p=InvestmentReturn.objects.get(date=dt,investment=self,freq=xs['freq'])
			except:
				p=InvestmentReturn()



			p.date=dt
			p.price=xs['P']
			p.prev_price=xs['PP']
			#p.xr=xs['XR']
			#p.prev_xr=xs['PXR']
			#p.dividend=xs['D']
			p.investment=self
			p.freq=xs['freq']

			

			p.save()


		return


	def create_and_save_returns_frame(self):

		enddate=datetime.today()

		#load prices
		pdf=self.load_price_frame(None,enddate)
		#bmpdf=self.bm.load_price_frame(None,enddate)

		
		if pdf is None:
			return None

		freqs=['d','m','y']
		for f in freqs:
			print 'generating returns for freq %s' % f
			try:
				if f=='m':
					cdf=pdf.asfreq(MonthEnd(),method='pad')

				elif f=='y':
					cdf=pdf.asfreq(YearEnd(),method='pad')

				else:
					cdf=pdf


				data={
					'P':cdf['price'],
					'PP':cdf['price'].shift(1),
					#'D':pdf['dividend'],
					'freq': f,
				}

				df=ps.DataFrame(data,index=cdf.index)

				self.save_returns_frame(df)
			except:
				print 'Insufficient data for freq %s' % f

		return


	def return_as_at(self,date,freq=None):

		df=self.load_returns_frame(freq)

		if freq=='y':
			date=date-YearEnd()

		elif freq=='m':
			date=date-MonthEnd()

		else:
			pass

	

		if df is None:
			return None

		try:
			r=df['TR']
			return round(r[date],4)
		except:
			print 'could not find return as at %s' % date
			return None
		
	def _latest_return(self):
	
		r=self.return_as_at(datetime.combine(self.latest_price_date,time()))
		
		return r
		
	latest_return = property(_latest_return)	

	def _latest_return_m(self):
	
		r=self.return_as_at(datetime.combine(self.latest_price_date,time()),'m')
		
		return r
		
	latest_return_m = property(_latest_return_m)	
	
	def _latest_return_y(self):
	
		r=self.return_as_at(datetime.combine(self.latest_price_date,time()),'y')
		
		return r
		
	latest_return_y = property(_latest_return_y)
	
	

		