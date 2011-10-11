from django.db import models
import pandas as ps
import numpy as np

from openportfolioapp.utils import full_name
from openportfolioapp.models.trade import Trade
from openportfolioapp.models.investment import Investment
from decimal import *
from pandas.core.datetools import DateOffset,MonthEnd,YearEnd
from openportfolioapp.models.prices import PortfolioPrice
from datetime import *
from openportfolioapp.utils.returns import returns_dmy
from openportfolioapp.utils.returns import geometric_return
from openportfolioapp.models.returns import PortfolioReturn


DEFAULT_CURRENCY='AUD'

class Portfolio(models.Model):
	
	""" A portfolio object
	"""
	
	class Meta:
		app_label = "openportfolioapp"
	
	name = models.CharField(max_length=255)
	parent = models.ForeignKey('self',blank=True,null=True,related_name='child')
	bm=models.ForeignKey('self',null=True,related_name='benchmark',blank=True)
	
	def _full_name(self):
		return full_name(self)
		
	full_name=property(_full_name)

	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return self.full_name
		
		

	

	def trades(self,dt,startdate=None,trade_type=None):
		
		if startdate is None:
			trns=Trade.objects.filter(date__lte=dt,portfolio=self)	
		else:
			trns=Trade.objects.filter(date__lte=dt,date__gte=startdate,portfolio=self)	
	
		if trade_type is not None:
			trns=trns.filter(trade_type=trade_type)
	
		for c in self.child.all():
			trns = trns | c.trades(dt,startdate,trade_type)

		return trns

	def load_holdings_frame_as_at(self,dt,curr=None):
		
		""" Returns a portfolio data frame as at a given date in a given currency
		
			Investment 1	Price 1		Port Holding 1		Benchmark Holding 1
			...
			Investment n	Price n		Port Holding n		Benchmark Holding n
		
		"""
		
		#make curr the default currency, should be handled in global settings
		if curr is None:
			curr=DEFAULT_CURRENCY
		

		bm=self.bm
		
		#we're dealing with a benchmark
		if bm is None:
			bm=self
			
		#we're going to build up holdings for transactions
		p_trns=self.trades(dt)
		b_trns=bm.trades(dt)
		combined_trns = p_trns | b_trns

		#unique investments in either the benchmark or portfolio
		unique_i = Investment.objects.filter(pk__in=combined_trns.values_list('investment').distinct())
		
		data={	'Hp': [],
				'Hb':[],
				'P':[],
				'XR':[],
				'I':[],
				'PP':[],
				'R':[],
				
			}
			
		#map investment price data to portfolio data frame
		ipdf_mappings={'P':'close','XR':'crossrate','I':'dividend'}
	
		for i in unique_i:

			#build holdings from transactions
			h=0
			for t in p_trns.filter(investment=i):
				h+=t.volume
			data['Hp'].append(h)

			#weighted purchase price
			wp=0
			for t in p_trns.filter(investment=i):
				wp+=(t.volume/h)*t.price

			data['PP'].append(wp)

			h=0
			for t in b_trns.filter(investment=i):
				h+=t.volume

			data['Hb'].append(h)
	
			ipdf=i.load_price_frame(dt,dt,curr)

			#get data from the price frame according to mapping
			for key,val in ipdf_mappings.iteritems():
				try:
					data[key].append(ipdf[ipdf_mappings[key]][0])
				except:
					data[key].append(0)
					
			r=i.return_as_at(dt,'m')
			
			if r is None:
				data['R'].append(0)
			else:
				data['R'].append(r)

		df=ps.DataFrame(data,index=unique_i)


		df['R']=df['R'].applymap(Decimal)
		
		df['P_fc']=df['P']*df['XR']
		df['PP_fc']=df['PP']*df['XR']
		df['MVp']=df['Hp']*df['P']
		df['MVb']=df['Hb']*df['P']
		df['MVp_fc']=df['Hp']*df['P_fc']
		df['MVb_fc']=df['Hb']*df['P_fc']
		df['PL']=(df['P_fc']-df['PP_fc'])*df['Hp']
	
		
		
		try:
			df['Wp']=df['MVp_fc']/df['MVp_fc'].sum()
		except:
			df['Wp']=df['MVp_fc']*0
		
		try:
			df['Wb']=df['MVb_fc']/df['MVb_fc'].sum()
		except:
			df['Wb']=df['MVb_fc']*0	
	
	
		df['Wa']=df['Wp']-df['Wb']
		df['Rp']=df['R']*df['Wp']
		return df
		
	def load_holdings_frame(self,startdate,enddate,curr=None):
		
		dates=ps.DateRange(startdate,enddate,offset=DateOffset(days=1))
		
		data={'frame':[],
			  'MVp': [],
			  'NumHoldings': [],
			}
		for dt in dates:
			print "...building %s" % dt.date()
			df=self.load_holdings_frame_as_at(dt,curr)
			
			if df is None:
				return None
				
			data['frame'].append(df)
			data['MVp'].append(df['MVp'].sum())
			data['NumHoldings'].append(df.index.size)
		
		hf=ps.DataFrame(data,index=dates)

		return hf
		
		
	def save_holdings_frame(self,df):
		
		if df is None:
			return

		for dt in df.index:

			try:
				p=PortfolioPrice.objects.get(date=dt,portfolio=self)
			except:
				p=PortfolioPrice()

			xs=df.xs(dt)

			p.date=dt
			p.marketvalue=xs['MVp']
			p.numholdings=xs['NumHoldings']
			p.price=p.marketvalue
			p.portfolio=self

			p.save()
		
		
		return
		
	def market_value_as_at(self,dt,curr=None):
		
		df=self.load_holdings_frame_as_at(dt,curr)
		
		try:
			return df['MVp'].sum()
		except:
			return None



	def load_returns_frame(self,freq='d'):
		
		qs=PortfolioReturn.objects.filter(portfolio=self,freq=freq)
		

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

			print '...saving returns frame %s' % dt
			xs=df.xs(dt)
		
			try:
				p=PortfolioReturn.objects.get(date=dt,portfolio=self,freq=xs['freq'])
			except:
				p=PortfolioReturn()

			

			p.date=dt
			p.price=xs['P']
			p.prev_price=xs['PP']
			#p.xr=xs['XR']
			#p.prev_xr=xs['PXR']
			#p.dividend=xs['D']
			p.portfolio=self
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
			
		r=df['return']

		if r is None:
			return None

		try:
			return round(r[date],4)
		except:
			print 'could not find return as at %s' % date
			return None

	def _latest_return(self):
		try:
			dt=datetime.combine(self.latest_price_date,time())
		except:
			return None
		
		r=self.return_as_at(dt)

		return r

	latest_return = property(_latest_return)	

	def _latest_return_m(self):

		try:
			dt=datetime.combine(self.latest_price_date,time())
		except:
			return None

		r=self.return_as_at(dt,'m')

		return r

	latest_return_m = property(_latest_return_m)	

	def _latest_return_y(self):

		try:
			dt=datetime.combine(self.latest_price_date,time())
		except:
			return None
			
		r=self.return_as_at(dt,'y')

		return r

	latest_return_y = property(_latest_return_y)
	
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
	

	def load_price_frame(self,startdate,enddate,crosscurr='USD'):
		
		
		if startdate==enddate:
			startdate=startdate-timedelta(days=5)
		
		if startdate==None:
			#all data up to enddate
			qs=PortfolioPrice.objects.filter(date__lte=enddate,portfolio=self).order_by('date')
		else:
			qs=PortfolioPrice.objects.filter(date__lte=enddate,date__gte=startdate,portfolio=self).order_by('date')
	
		if len(qs)==0:
			print "No prices found: %s" % self
			return None
				
		vlqs = qs.values_list()
		
	
			
		
		prices = np.core.records.fromrecords(vlqs, names=[f.name for f in PortfolioPrice._meta.fields])
		
		dates = [datetime.combine(d,time()) for d in prices.date]
	
		
		data={
			'price': prices.price,
			'marketvalue': prices.marketvalue,
			'numholdings': prices.numholdings,
		}
		
		pdf=ps.DataFrame(data,index=dates)	
		
		
		return pdf

	
	def mean(self):
		
		enddate=datetime.today()
		
		pdf=self.load_price_frame(None,enddate)
		
		return pdf['price'].applymap(float).mean()
		
	def price_as_at(self,date):
		
		p=PortfolioPrice.objects.filter(date__lte=date,portfolio=self).order_by('-date')


		if len(p)==0:
			return None

		p=p[0]
		return p.price,p.date		


	def dividend_as_at(self,date):
		#p=PortfolioPrice.objects.filter(date__lte=date,portfolio=self,dividend__gt=0).order_by('-date')
		p=[]
		if len(p)==0:
			return None

		p=p[0]
		return p.dividend,p.date