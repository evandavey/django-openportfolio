from django.conf.urls.defaults import *
from openportfolioapp.models import Investment,Portfolio
from django.views.generic import DetailView, ListView
from django.conf import settings


urlpatterns = patterns('',

(r'^$',
        ListView.as_view(
            queryset=Investment.objects.all,
            context_object_name='investment_list',
            template_name='openportfolioapp/index.html')),

(r'^investment/$',
        ListView.as_view(
            queryset=Investment.objects.all,
            context_object_name='investment_list',
            template_name='openportfolioapp/investment_list.html')),


(r'^portfolio/$',
       ListView.as_view(
            queryset=Portfolio.objects.all,
            context_object_name='portfolio_list',
            template_name='openportfolioapp/portfolio_list.html')),





(r'^test/$', 
	'openportfolioapp.views.returns_table',
	None,
	'returns_table'),

)

"""
URLS - Portfolio
"""
urlpatterns += patterns('openportfolioapp.views.portfolio',
  (r'^portfolio/(?P<portfolio_id>\d+)/report/(?:(?P<currency>\w+)/(?P<dt>\d+)/)?$', 
  	'report',
  	None,
  	'portfolio_report'),
  
)



"""
URLS - Investment
"""
urlpatterns += patterns('openportfolioapp.views.investment',
  (r'^investment/(?P<investment_id>\d+)/report/(?:(?P<enddate>\d+)/(?P<startdate>\d+)/)?$',
		'report',
		None,
		'investment_report'),
)
