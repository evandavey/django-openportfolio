from django.http import HttpResponse
from django.template import Context, loader

from django.contrib.auth.decorators import login_required
	
from django.views.generic.list_detail import object_detail
from openportfolioapp.models import Portfolio,Currency

from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from datetime import *

from pandas.core.datetools import MonthEnd


def holdings_table(request,portfolio_id,currency='AUD',dt=None):

	
		portfolio=Portfolio.objects.get(pk=portfolio_id)
		
		if dt is None:
			dt=datetime.today()
			df,dfm,dfy=portfolio._make_data_frame(dt,currency)

		else:
			dt=datetime.strptime(dt,'%Y%m%d')
			df,dfm,dfy=portfolio._make_data_frame(dt,currency)
			
		import numpy as np


		#generate a holdings data array more friendly to the template
		d=[]
		
		for i in df.index:
			
			x={}
			x['investment']=i
	
			
			for key,value in df.xs(i).iteritems():
				x[key]=value
			
			for key,value in dfm.xs(i).iteritems():
				x["m_"+key]=value
				
			for key,value in dfy.xs(i).iteritems():
				x["y_"+key]=value
				
			d.append(x)
			


		totals={
			'MV_fc': df['MV_fc'].sum(),
			'Hp': df['Hp'].sum(),
			'Hb': df['Hb'].sum(),
			'Wp': df['Wp'].sum(),
			'Wb': df['Wb'].sum(),
			'Wa': df['Wa'].sum(),
			'm_TR_fc': (df['Wp']*dfm['TR_fc']).sum(),
			'm_IR_fc': (df['Wp']*dfm['IR_fc']).sum(),
			'm_TRa_fc': (df['Wp']*dfm['TRa_fc']).sum(),
			'm_CR': (df['Wp']*dfm['CR']).sum(),
		
		}

		ct={'holdings_data':d,
			'totals': totals,
			'report_currency': Currency.objects.get(pk=currency).locale_code,

		}
		
	
		t = loader.get_template('openportfolioapp/holdings_table.html')

		
		return t.render(Context(ct))

@login_required(login_url='/openportfolioapp/accounts/login')
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)


@login_required(login_url='/openportfolioapp/accounts/login')
def portfolio_analysis(request,portfolio_id,currency='GBP',dt=None):
	
	portfolio=Portfolio.objects.get(pk=portfolio_id)
	
	end_dt=datetime.strptime(dt,'%Y%m%d')-MonthEnd()
	start_dt=end_dt-2*MonthEnd()
	
	
	
	holdings=holdings_table(request,portfolio_id,currency,end_dt.strftime('%Y%m%d'))
	
	ct={'portfolio':portfolio,
		'holdings_table':holdings,
		'report_currency': Currency.objects.get(pk=currency).locale_code,
		'report_currency_code': Currency.objects.get(pk=currency).code,
		'end_dt':end_dt,
		'start_dt':start_dt,
		
	}


	return render_to_response('openportfolioapp/portfolio_analysis.html',ct,context_instance=RequestContext(request))
	

def portfolio_barchart(request,portfolio_id,analysis_field,currency='AUD',dt=None):

	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	import numpy as np
	import matplotlib.pyplot as plt
	import pylab
	from matplotlib.patches import Polygon
	from matplotlib.ticker import MaxNLocator


	

	#load data frame
	
	p=Portfolio.objects.get(pk=portfolio_id)
	
	
	print 'Barchart date is ' + dt
	
	if dt is None:
		dt=datetime.today()
		df,dfm,dfy=p._make_data_frame(dt,currency)
		
	else:
		dt=datetime.strptime(dt,'%Y%m%d')
		df,dfm,dfy=p._make_data_frame(dt,currency)

	
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

