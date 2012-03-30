from datetime import *
from django.template import Context, loader
from django.shortcuts import render_to_response,redirect
from django.template.loader import render_to_string
from django.http import HttpResponse

from django.template import RequestContext
from openportfolioapp.models import Portfolio,Currency,Trade
from pandas.core.datetools import MonthEnd,YearEnd

from django.contrib.auth.decorators import login_required

DEFAULT_CURRENCY='AUD'
DEFAULT_ANALYSIS_FIELD='asset_class'

import sys
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError 

import threading

class PortfolioReportThread(threading.Thread):
    
    def __init__(self,cache_key,request,portfolio_id,currency,dt,start_dt):
        threading.Thread.__init__(self)
        self.max_count=10
        self.count=0.0
        self.cache_key=cache_key
        self.portfolio_id=portfolio_id
        self.currency=currency
        self.dt=dt
        self.start_dt=start_dt
        self.request=request
               
        
    def run(self):
        
        portfolio_id=self.portfolio_id
        currency=self.currency
        dt=self.dt
        start_dt=self.start_dt
        request=self.request
        
        cache_key=self.cache_key
        data = cache.get(cache_key)

        data['pct_progress']=0.05
        data['message']="loading holdings table"
        
        cache.set(cache_key,data)
        portfolio=Portfolio.objects.get(pk=portfolio_id)


        if currency is None:
            currency=DEFAULT_CURRENCY

        if dt is None:
            dt=datetime.today()-MonthEnd()
        else:
            dt=datetime.strptime(dt,'%Y%m%d')

        end_dt=datetime(dt.year,dt.month,1)+MonthEnd()

        if start_dt is None:
            start_dt=end_dt-MonthEnd()
        else:
            start_dt=datetime.strptime(start_dt,'%Y%m%d')
            
        print "Lading report for %s,%s" % (start_dt,end_dt)

        ht=None
        rt1=None
        pc=None
        
        try:
            rc=Currency.objects.get(code=currency)
            ht=portfolio.holdings_table(start_dt,end_dt,rc)
            print 'holdings table loaded'
            data['pct_progress']=0.5
            data['message']="loading price table"
            cache.set(cache_key,data)
            pt=portfolio.price_table(start_dt,end_dt,rc)
            print 'price table loaded'
            
            data['pct_progress']=0.75
            data['message']="loading risk table"
            
            cache.set(cache_key,data)
            rt1=portfolio.riskbucket_table(start_dt,end_dt,rc,'assetclass')
            data['message']="loading price chart"
            
            data['pct_progress']=0.80
            cache.set(cache_key,data)
            pc=portfolio.price_chart(end_dt)
            ct={'portfolio':portfolio,
                    'holdings_table':ht,
                    'price_table':pt,
                    'report_currency': rc,
                    'end_dt':end_dt,
                    'start_dt':start_dt,
                    'risk_table1': rt1,
                    'price_chart': pc,

            }


            data['message']="rendering"
            result=render_to_string('openportfolioapp/portfolio/report.html',ct,context_instance=RequestContext(request))
            data['portfolio']=portfolio
            
        except:
            data['message']="Caught an error %s:%s" % (sys.exc_info()[0],sys.exc_info()[1])
            print data['message']
            result="ERROR: %s:%s" % (sys.exc_info()[0],sys.exc_info()[1])
            
            data['pct_progress']=0.9
            

        
        data['result']=result
        data['pct_progress']=1.0
        cache.set(cache_key,data)
        print 'rendering done'
        



@login_required(login_url='/accounts/login')
def list(request):


    ct={'portfolio_list':Portfolio.objects.all()}


    return render_to_response('openportfolioapp/portfolio/list.html',ct,context_instance=RequestContext(request))



@login_required(login_url='/accounts/login')
def report(request,portfolio_id,currency=None,dt=None,startdate=None):

    """
    Uses a wrapper process and a data retrieval thread to allow a progress bar to be displayed.
    """
   
    progress_id = ''
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
        
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    
    if progress_id:
        from django.utils import simplejson
        
        
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        #print "key: %s" % cache_key
        data = cache.get(cache_key)
     
        #print data
        
        if data is None:
            #print "Data empty, setting cache"
            cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
            data={
                   'pct_progress': 0.0,
                   'done': 0,
                   'msg':'starting load',
            }
            cache.set(cache_key, data)
            t = PortfolioReportThread(cache_key,request,portfolio_id,currency,dt,startdate)
            t.start()
            return HttpResponse(simplejson.dumps(data))
        else:
            
            if data['done']==0 and data['pct_progress']>=1:
                
                data['done']=1
                cache.set(cache_key, data)
                
                data={'done':1,'result':data['result']}
                json=simplejson.dumps(data)
                
                return HttpResponse(json)
                
            elif int(data['done'])==1:
                 #print 'deleted cache'
                 cache.delete(cache_key)
                 
            else:
                cache.set(cache_key, data)
                return HttpResponse(simplejson.dumps(data))
    else:
        
        
        if currency is None:
            currency=DEFAULT_CURRENCY

        if dt is None:
            dt=datetime.today()-MonthEnd()
        else:
            dt=datetime.strptime(dt,'%Y%m%d')

        end_dt=datetime(dt.year,dt.month,1)+MonthEnd()

        if startdate is None:
            startdate=end_dt-MonthEnd()
    
    
        progress_url=request.path_info
    
        ct={'progress_url':progress_url
        
        }
        return render_to_response('openportfolioapp/progress-wrapper.html',ct,context_instance=RequestContext(request))
