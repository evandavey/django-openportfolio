from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


from datetime import *

from openportfolioapp.models import Investment
from pandas.core.datetools import MonthEnd

@login_required(login_url='/accounts/login')
def list(request):
 

    ct={'investment_list':Investment.objects.all()}


    return render_to_response('openportfolioapp/investment/list.html',ct,context_instance=RequestContext(request))


@login_required(login_url='/accounts/login')
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
		
	}


	return render_to_response('openportfolioapp/investment/report.html',ct,context_instance=RequestContext(request))
	
