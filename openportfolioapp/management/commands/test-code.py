from django.core.management.base import BaseCommand, CommandError
from openportfolioapp.models import *

from pandas.core.datetools import MonthEnd
from datetime import datetime
import numpy as np
from openportfolioapp.utils.returns import geometric_return
def return_agg(x):
	
	x=x+1
	return x.prod()-1
	
	

class Command(BaseCommand):
	args = '<start_date YYYYMMDD> <end_date YYYYMMDD>'
	help = 'Fetches porfolio prices'

	def handle(self, *args, **options):
		
		i=Investment.objects.filter(pk=9)
		i=i[0]

		df,dfm,dfy=i.load_returns_frame()


		#g=df.applymap(float).groupby(lambda x: x+MonthEnd()).agg([np.mean,return_agg])
		g=df.applymap(float).groupby(lambda x: datetime(x.year,x.month,1)+MonthEnd()).agg([np.mean,geometric_return,np.max,np.min])
		
		
		for dt in g.index:
			xs=g.xs(dt)
			for x in xs.flat:
				print x
			
		# for name,group in g:
		# 			print name
		# 			print group
		# 		


