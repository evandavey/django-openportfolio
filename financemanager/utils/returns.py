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

	g_m=df.applymap(float).groupby(lambda x: datetime(x.year,x.month,1)+MonthEnd())
	g_y=df.applymap(float).groupby(lambda x: datetime(x.year,12,1)+MonthEnd())
	
	
	for idx,group in g_m:
		print geometric_return(group['price'])
	
	
	

def returns(df,idx,idx2=None):
	"""
    compute the daily return of idx in x

	x is a pandas dateframe object
	
	idx2 can be used instead to calculate
	a return on idx1 eg: for dividends

    """

	prices=df[idx].applymap(float)
	prev_prices=df[idx].shift(1).applymap(float)
	
	if idx2 is not None:
		prices2=df[idx2].applymap(float)
		r=prices2/prev_prices
		idx=idx2
	else:
		r=(prices-prev_prices)/prev_prices
	
	r=r.applymap(Decimal)
	df[idx+ '_return']=r
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