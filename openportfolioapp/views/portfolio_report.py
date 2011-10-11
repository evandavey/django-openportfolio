from datetime import *
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.template import RequestContext
from openportfolioapp.models import Portfolio,Currency,Trade
from pandas.core.datetools import MonthEnd,YearEnd
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from openportfolioapp.views.returns import returns_table

DEFAULT_CURRENCY='AUD'
DEFAULT_ANALYSIS_FIELD='asset_class'

def portfolio_report(request,portfolio_id,currency='AUD',dt=None,startdate=None):
	
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
	
	ctpk = ContentType.objects.get_for_model(portfolio).id
	
	returns=returns_table(request,portfolio_id,ctpk,'m')
	holdings=holdings_table(request,portfolio_id,currency,end_dt.strftime('%Y%m%d'),portfolio)	
	trades=trades_table(request,portfolio_id,start_dt,end_dt,portfolio)
	
	ct={'portfolio':portfolio,
		'holdings_table':holdings,
		'report_currency': Currency.objects.get(pk=currency).locale_code,
		'report_currency_code': Currency.objects.get(pk=currency).code,
		'end_dt':end_dt,
		'start_dt':start_dt,
		'returns_table':returns,
		'trades_table':trades,
		
	}


	return render_to_response('openportfolioapp/portfolio_report.html',ct,context_instance=RequestContext(request))


def trades_table(request,portfolio_id,startdate=None,enddate=None,portfolio=None):
			
		if portfolio is None:
			portfolio=Portfolio.objects.get(pk=portfolio_id)

		if startdate is None:
			startdate=datetime.today()
	
	
			
		
		trds=portfolio.trades(enddate,startdate)
		
		
		ct={'trades': trds,
		}

		t = loader.get_template('openportfolioapp/tradetable.html')

		return t.render(Context(ct))

	
def holdings_table(request,portfolio_id,currency='AUD',dt=None,portfolio=None):

	
	
		if currency is None:
			currency=DEFAULT_CURRENCY
			
		if portfolio is None:
			portfolio=Portfolio.objects.get(pk=portfolio_id)

		if dt is None:
			dt=datetime.today()
		else:
			dt=datetime.strptime(dt,'%Y%m%d')
		
		
		df=portfolio.load_holdings_frame_as_at(dt,currency)
	
		print df['P']
		
		fields=[
			{'label':'Market Value','key':'MVp_fc','total':'sum','format':'rc'},
			{'label':'Price','key':'P_fc','total':None,'format':'rc'},
			{'label':'Price','key':'P','total':None,'format':'lc'},
			{'label':'Hp','key':'Hp','total':'sum','format':'{0:.2f}'},
			{'label':'Hb','key':'Hb','total':'sum','format':'{0:.2f}'},
			{'label':'Wp','key':'Wp','total':'sum','format':'{0:.2%}'},
			{'label':'Wb','key':'Wb','total':'sum','format':'{0:.2%}'},
			{'label':'Purchase Price','key':'PP','total':None,'format':'lc'},
			{'label':'P&L','key':'PL','total':'sum','format':'rc'},
			{'label':'Rp','key':'Rp','total':'sum','format':'{0:.2%}'},
			]

		ct={'report_currency': Currency.objects.get(pk=currency),
			'df': df,
			'fields': fields,
		}

		t = loader.get_template('openportfolioapp/holdingstable.html')

		return t.render(Context(ct))
		


def portfolio_barchart(request,portfolio_id,analysis_field,currency='AUD',dt=None,p=None):

	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	import numpy as np
	import matplotlib.pyplot as plt
	import pylab
	from matplotlib.patches import Polygon
	from matplotlib.ticker import MaxNLocator

	if currency is None:
		currency=DEFAULT_CURRENCY

	if analysis_field is None:
		analysis_field=DEFAULT_ANALYSIS_FIELD


	#load data frame

	if p is None:
		p=Portfolio.objects.get(pk=portfolio_id)

	if dt is None:
		dt=datetime.today()
		dt=dt-MonthEnd()
	else:
		dt=datetime.strptime(dt,'%Y%m%d')
	
	df=p.load_holdings_frame_as_at(dt,currency)

	if analysis_field=='asset_class':
		g=df.groupby(lambda d: d.asset_class.name).aggregate(np.sum)
	elif analysis_field=='gics_sector':
		g=df.groupby(lambda d: d.company.gics_sector.name).aggregate(np.sum)
	elif analysis_field=='company':
		g=df.groupby(lambda d: d.company.name).aggregate(np.sum)


	N = len(g)

	names = g['Wa'].index
	active = g['Wa']*100
	port = g['Wp']*100
	bm = g['Wb']*100

	height=0.1
	fig = plt.figure(figsize=(10,5),facecolor='w')


	ax1 = fig.add_subplot(111)
	plt.subplots_adjust(left=0.2, right=0.75)

	pos = (np.arange(N)+(height*3))    #Center bars on the Y-axis ticks
	rects2 = ax1.barh(pos-height, active, align='center', height=height, color='#003366')
	rects = ax1.barh(pos, port, align='center', height=height, color='r')
	rects1 = ax1.barh(pos+height, bm, align='center', height=height, color='g')

	plt.legend( (rects[0], rects1[0], rects2[0]), ('Portfolio', 'Benchmark','Active') ,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	ax1.axis([-100,100,0,N])

	pylab.yticks(pos, names)
	ax1.xaxis.set_major_locator(MaxNLocator(11))
	plt.plot([0,0], [0, 5], 'black', alpha=1)



	def on_draw(event):
	   bboxes = []
	   for label in labels:
	       bbox = label.get_window_extent()
	       # the figure transform goes from relative coords->pixels and we
	       # want the inverse of that
	       bboxi = bbox.inverse_transformed(fig.transFigure)
	       bboxes.append(bboxi)

	   # this is the bbox that bounds all the bboxes, again in relative
	   # figure coords
	   bbox = mtransforms.Bbox.union(bboxes)
	   if fig.subplotpars.left < bbox.width:
	       # we need to move it over
	       fig.subplots_adjust(left=1.1*bbox.width) # pad a little
	       fig.canvas.draw()
	   return False

	fig.canvas.mpl_connect('draw_event', on_draw)


	canvas=FigureCanvas(fig)
	response=HttpResponse(content_type='image/png')
	canvas.print_png(response)
	return response