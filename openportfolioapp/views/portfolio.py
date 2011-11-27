from datetime import *
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.template import RequestContext
from openportfolioapp.models import Portfolio,Currency,Trade
from pandas.core.datetools import MonthEnd,YearEnd

from django.contrib.auth.decorators import login_required

DEFAULT_CURRENCY='AUD'
DEFAULT_ANALYSIS_FIELD='asset_class'


@login_required(login_url='/accounts/login')
def list(request):
 

    ct={'portfolio_list':Portfolio.objects.all()}


    return render_to_response('portfolio/list.html',ct,context_instance=RequestContext(request))

@login_required(login_url='/accounts/login')
def report(request,portfolio_id,currency='AUD',dt=None,startdate=None):
	
	portfolio=Portfolio.objects.get(pk=portfolio_id)
	
	
	if currency is None:
		currency=DEFAULT_CURRENCY
		
	if dt is None:
		dt=datetime.today()-MonthEnd()
	else:
		dt=datetime.strptime(dt,'%Y%m%d')
	
		
	end_dt=datetime(dt.year,dt.month,1)+MonthEnd()
	
	if startdate is None:
		start_dt=end_dt-MonthEnd()
	
	
	rc=Currency.objects.get(pk=currency)
	
	ct={'portfolio':portfolio,
		'holdings_table':portfolio.holdings_table(start_dt,end_dt,rc),
		'price_table':portfolio.price_table(start_dt,end_dt,rc),
		'report_currency': rc.locale_code,
		'report_currency_code': rc.code,
		'end_dt':end_dt,
		'start_dt':start_dt,

	}


	return render_to_response('portfolio/report.html',ct,context_instance=RequestContext(request))

