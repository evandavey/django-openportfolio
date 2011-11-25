from django.shortcuts import render_to_response
from django.template import RequestContext

from datetime import *

from openportfolioapp.models import Investment
from pandas.core.datetools import MonthEnd



def report(request,investment_id,enddate=None,startdate=None):
	
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
		#'returns': returns_table(request,investment_id,investment.content_type.id),
		
	}


	return render_to_response('investment/report.html',ct,context_instance=RequestContext(request))
	
