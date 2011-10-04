from datetime import *
from financemanager.models import Investment
from pandas.core.datetools import MonthEnd
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import pandas
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from financemanager.utils.charts import chart_technical_analysis
from financemanager.views.returns import returns_table

def investment_report(request,investment_id,enddate=None,startdate=None):
	
	#workaround subclassing not working on objects.get()
	investment=Investment.objects.filter(pk=investment_id)
	investment=investment[0]
	
	if enddate is None:
		enddate = datetime.today()
		
	else:
		enddate=datetime.strptime(enddate,'%Y%m%d')
		
	if startdate is None:
		startdate = enddate-12*MonthEnd()
	else:
		startdate=datetime.strptime(startdate,'%Y%m%d')

	
	ct={'object':investment,
		'end_dt':enddate,
		'start_dt':startdate,
		'returns': returns_table(request,investment_id,investment.content_type.id),
		
	}


	return render_to_response('financemanager/investment_report.html',ct,context_instance=RequestContext(request))
	


def investment_chart(request,investment_id,enddate,startdate=None,i=None):
	

	if i is None:
		#workaround subclassing not working on objects.get()
		i=Investment.objects.filter(pk=investment_id)
		i=i[0]
		
	if enddate is None:
		enddate = datetime.today()
		
	else:
		enddate=datetime.strptime(enddate,'%Y%m%d')
		
	if startdate is None:
		startdate = enddate-24*MonthEnd()
	else:
		startdate=datetime.strptime(startdate,'%Y%m%d')
		

	print i
	df=i.load_price_frame(startdate,enddate)
	
	if df is None:
		return None
	
	r=df.applymap(float).toRecords()
	 

	fig=chart_technical_analysis(r,i.full_ticker,startdate,enddate)

	canvas=FigureCanvas(fig)
	response=HttpResponse(content_type='image/png')
	canvas.print_png(response)
	return response