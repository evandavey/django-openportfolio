from datetime import *
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.template import RequestContext
from financemanager.models import Portfolio,Currency,Investment
from pandas.core.datetools import MonthEnd
from django.http import HttpResponse
import numpy as np
from financemanager.utils.returns import geometric_return
from django.contrib.contenttypes.models import ContentType
import pandas as ps

def returns_table(request,pk,ctpk,date_format=None):
	
	
	ct = ContentType.objects.get(pk=ctpk)
	
	model = ct.model_class()
	
	i=model.objects.filter(pk=pk)
	i=i[0]
	
	
	rdf=i.load_returns_frame()
	
	if rdf is None:
		return None


	if model == Portfolio:
		#df=rdf.filter(['TR','bm_price_return'])
		df=rdf.filter(['CR','TR'])
	else:
		df=rdf.filter(['IR','CR','TR'])

	
	print df

	
	if date_format=='m':
		grouped=df.applymap(float).groupby(lambda x: datetime(x.year,x.month,1)+MonthEnd())
		index_format='{:%Y %b}'
	else:
		grouped=df.applymap(float).groupby(lambda x: datetime(x.year,12,1)+MonthEnd())
		index_format='{:%Y}'
	
	grouped=grouped.aggregate(geometric_return)
	
	#work around since template doesn't seem to like datamatrix object
	idx=grouped.index
	
	
	fields=[
		{'key':'CR','format':'{0:.2%}','label':'Cap Return'},
		{'key':'IR','format':'{0:.2%}','label':'Inc Return'},
		{'key':'TR','format':'{0:.2%}','label':'Total Return'},
	]
	
	data={}
	avail_fields=[]
	for f in fields:	
		try:
			data[f['key']]=grouped[f['key']]
			avail_fields.append(f)
		except:
			pass
	
	df=ps.DataFrame(data,index=idx)
	

	
	try:
		df['TRa']=df['TR']-df['bm_TR']
		avail_fields.append({'key':'TRa','format':'{0:.2%}','label':'Active Return'})
	
	except:
		pass	
		
	ct={'df': df,
		'table_id': 'returns_table',
		'index_id': 'Date',
		'index_format': index_format,
		'fields': avail_fields,
	}

	t = loader.get_template('financemanager/dataframe_table.html')

	return t.render(Context(ct))

	

	
def returns_chart():

	pass
	
	
	