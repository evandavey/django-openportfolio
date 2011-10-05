import pandas as ps
from datetime import *
from decimal import *
import numpy as np
from pandas.core.datetools import MonthEnd,YearEnd

def weights(x):
	"""
    compute the weights of x

    """

	if x.sum()==0:
		return x*0
	else:
		return x/x.sum()
	

def geometric_return(x):
	"""
	compute the geometric return for a given series
	[(1+r1)(1+r2)...(1+rn)]-1	
	"""
	
	
	x=x+1
	x=x.prod()-1
	
	
	return x[0]

	
def returns_dmy(df):
	"""
	compute daily,monthly,yearly returns 
	
	"""


	r=returns(df)
	r_m=returns(df)
	r_y=returns(df)
	
	
	return r,r_m,r_y
	
	

def returns(df,idx={'P':'price','XR':'crossrate','D':'dividend'}):
	"""
    compute the return from a given dataframe

	idx is a dictionary mapping price,xrates and dividends
	
	sets TR,CR then CR_fc,IR,IR_fc if data available
	
	returns None if price data can not be found

    """

	try:
		prices=df[idx['P']].applymap(float)
		prev_prices=prices.shift(1)
	except:
		print 'Could not find price in dataframe'
		return None
	
	try:
		xr=df[idx['XR']].applymap(float)
		prices_fc=prices*xr
		prev_prices_fc=prices_fc.shift(1)
	except:
		prices_fc=None
		print 'Could not find price fc in dataframe'
		
	try:
		dividends=df[idx['D']].applymap(float)
	except:
		dividends=None
		print 'Could not find dividends in dataframe'	
		
	
	
	
	cap_return=((prices-prev_prices)/prev_prices).applymap(Decimal)
	df['CR']=cap_return
	

	
	
	if prices_fc is not None:
		cap_return_fc=((prices_fc-prev_prices_fc)/prev_prices_fc).applymap(Decimal)
		df['CR_fc']=cap_return_fc
	
	if dividends is not None:
		inc_return=(dividends/prev_prices).applymap(Decimal)
		df['IR']=inc_return
		
		if prices_fc is not None:
			dividends_fc=dividends*xr
			inc_return_fc=(dividends_fc/prev_prices_fc).applymap(Decimal)
			df['IR_fc']=inc_return_fc
			
	
	try:
		df['TR']=df['CR']+df['IR']
	except:
		df['TR']=df['CR']
		
	
	try:
		df['TR_fc']=df['CR_fc']+df['IR_fc']
	except:
		try:
			df['TR_fc']=df['CR_fc']
		except:
			pass

	
	return df
	


def beta(x, m):
	"""
	compute the beta of x vs the market m.

	beta(x) = cov(x,m) / var(m)

	x,m are timeseries objects

	"""

	#align series on dates
	x_a,y_a = ts.align_series(x,y)

	""" 
	matrix = [var(x), cov(x,mn)]
	[cov(m,x)], var(m)]
	"""

	matrix=np.cov(x_a,y_a)

	return matrix[0][1]/matrix[1][1]